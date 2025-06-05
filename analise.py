import pandas as pd
import numpy as np

def carregar_dados(caminho):
    df = pd.read_excel(caminho)
    # Padroniza nomes de colunas para facilitar o uso
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    return df

def tratar_datas(df):
    datas = [
        'chegada_na_barra', 'atracação', 'estimativa_atracação_etb',
        'início_operação', 'fim_operação', 'liberação_rfb', 'etb', 'etd'
    ]
    for col in datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def tempo_espera_barra_atracacao(df):
    # Tempo entre chegada na barra e atracação
    df['espera_barra_atracacao'] = (df['atracação'] - df['chegada_na_barra']).dt.total_seconds() / 3600
    return df[df['espera_barra_atracacao'] > df['espera_barra_atracacao'].quantile(0.75)][
        ['navio_/_viagem.1', 'chegada_na_barra', 'atracação', 'espera_barra_atracacao']
    ]

def atraso_etb_atracacao(df):
    # Diferença entre ETB previsto e real
    df['atraso_etb_atracacao'] = (df['atracação'] - df['estimativa_atracação_etb']).dt.total_seconds() / 3600
    return df[df['atraso_etb_atracacao'] > 1][
        ['navio_/_viagem.1', 'berço', 'estimativa_atracação_etb', 'atracação', 'atraso_etb_atracacao']
    ]

def tempo_permanencia_porto(df):
    # Tempo do início ao fim da operação
    df['tempo_porto'] = (df['fim_operação'] - df['início_operação']).dt.total_seconds() / 3600
    media = df['tempo_porto'].mean()
    return df[df['tempo_porto'] > media][
        ['navio_/_viagem.1', 'início_operação', 'fim_operação', 'tempo_porto']
    ]

def concentracao_navios_aguardando(df):
    # Conta quantos navios estavam aguardando operação por dia
    df = df.dropna(subset=['chegada_na_barra', 'atracação'])
    dias = pd.date_range(df['chegada_na_barra'].min(), df['atracação'].max(), freq='D')
    concentracao = []
    for dia in dias:
        aguardando = ((df['chegada_na_barra'] <= dia) & (df['atracação'] > dia)).sum()
        concentracao.append({'data': dia, 'navios_aguardando': aguardando})
    return pd.DataFrame(concentracao)

def liberacao_rfb_atrasada(df):
    # Liberação RFB após o fim da operação
    df['atraso_rfb'] = (df['liberação_rfb'] - df['fim_operação']).dt.total_seconds() / 3600
    return df[df['atraso_rfb'] > 1][
        ['navio_/_viagem.1', 'fim_operação', 'liberação_rfb', 'atraso_rfb']
    ]

if __name__ == '__main__':
    df = carregar_dados('ProgramacaoDeNavios.xlsx')
    df = tratar_datas(df)
    # Salva as análises em arquivos auxiliares para uso no dashboard
    tempo_espera_barra_atracacao(df).to_csv('espera_barra_atracacao.csv', index=False)
    atraso_etb_atracacao(df).to_csv('atraso_etb_atracacao.csv', index=False)
    tempo_permanencia_porto(df).to_csv('tempo_permanencia_porto.csv', index=False)
    concentracao_navios_aguardando(df).to_csv('concentracao_navios_aguardando.csv', index=False)
    liberacao_rfb_atrasada(df).to_csv('liberacao_rfb_atrasada.csv', index=False)