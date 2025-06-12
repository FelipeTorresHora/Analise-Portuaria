import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_data(path):
    """Carrega e processa os dados do arquivo Excel"""
    df = pd.read_excel(path)

    # Converter colunas para datetime
    df['Desatracação'] = pd.to_datetime(df['Desatracação'], format='%d/%m/%Y %H:%M')
    df['Atracação'] = pd.to_datetime(df['Atracação'], format='%d/%m/%Y %H:%M')
    df['Fim Operação'] = pd.to_datetime(df['Fim Operação'], format='%d/%m/%Y %H:%M')
    df['Início Operação'] = pd.to_datetime(df['Início Operação'], format='%d/%m/%Y %H:%M')

    # Calcular tempos
    df['Tempo no porto'] = df['Desatracação'] - df['Atracação']
    df['Tempo de Operação'] = df['Fim Operação'] - df['Início Operação']
    df['Tempo no porto H'] = df['Tempo no porto'].dt.total_seconds() / 3600
    df['Tempo de Operação H'] = df['Tempo de Operação'].dt.total_seconds() / 3600

    # Remover linhas onde 'Movs' é 0
    df = df[df['Movs'] != 0].copy()

    # Criar colunas 'Dia' e 'Mês'
    df['Dia'] = df['Atracação'].dt.date
    df['Mês'] = df['Atracação'].dt.strftime('%m/%Y')

    return df

def remover_outliers_iqr(df, coluna):
    """Remove outliers usando o método IQR"""
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr
    return df[(df[coluna] >= limite_inf) & (df[coluna] <= limite_sup)]

def grafico_tempo_medio(df):
    """Gráfico de tempo médio de estadia no porto vs tempo de operação"""
    # Agrupar dados por mês
    avg_data_mes = df.groupby('Mês').agg(
        {'Tempo Estadia Porto': 'mean', 'Tempo de Operação H': 'mean'}
    ).reset_index()

    # Derreter o DataFrame para formato long
    df_melted = avg_data_mes.melt(
        id_vars=['Mês'],
        value_vars=['Tempo Estadia Porto', 'Tempo de Operação H'],
        var_name='Métrica',
        value_name='Média de Horas'
    )

    # Criar gráfico com Plotly
    fig = px.bar(
        df_melted,
        x='Mês',
        y='Média de Horas',
        color='Métrica',
        barmode='group',
        title='Média de Horas Estadia no Porto e de Operação por Mês',
        labels={
            'Média de Horas': 'Média de Horas',
            'Métrica': 'Tipo de Tempo'
        },
        hover_name='Mês'
    )

    return fig

def grafico_tempo_medio_tratado(df):
    """Gráfico de tempo médio tratado (sem outliers)"""
    df_filtrado = remover_outliers_iqr(df, 'Tempo Estadia Porto')
    df_filtrado = remover_outliers_iqr(df_filtrado, 'Tempo de Operação H')

    avg_data_mes = df_filtrado.groupby('Mês').agg(
        {'Tempo Estadia Porto': 'mean', 'Tempo de Operação H': 'mean'}
    ).reset_index()

    df_melted = avg_data_mes.melt(
        id_vars=['Mês'],
        value_vars=['Tempo Estadia Porto', 'Tempo de Operação H'],
        var_name='Métrica',
        value_name='Média de Horas'
    )

    fig = px.bar(
        df_melted,
        x='Mês',
        y='Média de Horas',
        color='Métrica',
        barmode='group',
        title='Média de Horas Estadia no Porto e de Operação por Mês (Sem Outliers)',
        labels={
            'Média de Horas': 'Média de Horas',
            'Métrica': 'Tipo de Tempo'
        },
        hover_name='Mês'
    )

    return fig

def media_dif_estadia_operacao(df):
    """Gráfico de média da diferença entre estadia e operação"""
    monthly_avg_times = df.groupby('Mês').agg(
        avg_tempo_operacao=('Tempo de Operação H', 'mean'),
        avg_diferenca_nao_operacional=('Diferença Porto x Operação', 'mean')
    ).reset_index()

    df_melted_stack = monthly_avg_times.melt(
        id_vars=['Mês'],
        value_vars=['avg_tempo_operacao', 'avg_diferenca_nao_operacional'],
        var_name='Tipo de Tempo',
        value_name='Média de Horas'
    )

    df_melted_stack['Tipo de Tempo'] = df_melted_stack['Tipo de Tempo'].map({
        'avg_tempo_operacao': 'Tempo de Operação',
        'avg_diferenca_nao_operacional': 'Tempo Não-Operacional na Estadia'
    })

    fig = px.bar(
        df_melted_stack,
        x='Mês',
        y='Média de Horas',
        color='Tipo de Tempo', 
        title='Média de Tempo de Estadia no Porto: Operacional vs. Não-Operacional por Mês',
        labels={
            'Média de Horas': 'Média de Horas',
            'Tipo de Tempo': 'Tipo de Tempo'
        },
        hover_data={'Média de Horas': ':.2f'} 
    )

    return fig

def media_dif_estadia_operacao_tratado(df):
    """Gráfico de média da diferença entre estadia e operação (tratado)"""
    df_filtrado = remover_outliers_iqr(df, 'Tempo de Operação H')
    df_filtrado = remover_outliers_iqr(df_filtrado, 'Diferença Porto x Operação')

    monthly_avg_times = df_filtrado.groupby('Mês').agg(
        avg_tempo_operacao=('Tempo de Operação H', 'mean'),
        avg_diferenca_nao_operacional=('Diferença Porto x Operação', 'mean')
    ).reset_index()

    df_melted_stack = monthly_avg_times.melt(
        id_vars=['Mês'],
        value_vars=['avg_tempo_operacao', 'avg_diferenca_nao_operacional'],
        var_name='Tipo de Tempo',
        value_name='Média de Horas'
    )

    df_melted_stack['Tipo de Tempo'] = df_melted_stack['Tipo de Tempo'].map({
        'avg_tempo_operacao': 'Tempo de Operação',
        'avg_diferenca_nao_operacional': 'Tempo Não-Operacional na Estadia'
    })

    fig = px.bar(
        df_melted_stack,
        x='Mês',
        y='Média de Horas',
        color='Tipo de Tempo',
        barmode='stack',
        title='Média de Tempo de Estadia no Porto: Operacional vs. Não-Operacional por Mês (Sem Outliers)',
        labels={
            'Média de Horas': 'Média de Horas',
            'Tipo de Tempo': 'Tipo de Tempo'
        },
        hover_data={'Média de Horas': ':.2f'}
    )

    return fig

def grafico_movs_mes(df):
    """Gráfico de total de movimentações por mês"""
    total_movs_mes = df.groupby('Mês')['Movs'].sum().reset_index()

    fig = px.bar(
        total_movs_mes,
        x='Mês',
        y='Movs',
        title='Total de Movimentações (Movs) por Mês',
        labels={
            'Mês': 'Mês',
            'Movs': 'Total de Movimentações'
        },
        hover_name='Mês'
    )

    return fig

def grafico_horasxmovs_mes(df):
    """Gráfico comparativo de movimentações vs horas de operação"""
    monthly_totals = df.groupby('Mês').agg(
        total_movs=('Movs', 'sum'),
        total_tempo_operacao_h=('Tempo de Operação H', 'sum')
    ).reset_index()

    monthly_totals['Mês_ordenado'] = pd.to_datetime(monthly_totals['Mês'], format='%m/%Y')
    monthly_totals = monthly_totals.sort_values('Mês_ordenado').drop(columns='Mês_ordenado')

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=monthly_totals['Mês'],
            y=monthly_totals['total_movs'],
            name='Total de Movimentações',
            marker_color='mediumseagreen', 
            yaxis='y1' 
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_totals['Mês'],
            y=monthly_totals['total_tempo_operacao_h'],
            mode='lines+markers', 
            name='Total de Horas de Operação',
            marker_color='darkorange', 
            line=dict(width=3), 
            yaxis='y2' 
        )
    )

    fig.update_layout(
        title_text='Total de Movimentações vs. Total de Horas de Operação por Mês',
        xaxis_title='Mês',
        yaxis=dict(
            title='Total de Movimentações',
            side='left',
            showgrid=False 
        ),
        yaxis2=dict(
            title='Total de Horas de Operação',
            overlaying='y', 
            side='right' 
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def grafico_hipoteses(df):
    """Gráfico para análise da primeira hipótese"""
    monthly_summary_estadia = df.groupby('Mês').agg(
        total_movs=('Movs', 'sum'),
        total_tempo_estadia_h=('Tempo Estadia Porto', 'sum')
    ).reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=monthly_summary_estadia['Mês'],
            y=monthly_summary_estadia['total_movs'],
            name='Total de Movimentações',
            marker_color='royalblue',
            yaxis='y1'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_summary_estadia['Mês'],
            y=monthly_summary_estadia['total_tempo_estadia_h'],
            mode='lines+markers',
            name='Total de Estadia no Porto (Horas)',
            marker_color='purple',
            line=dict(width=3),
            yaxis='y2'
        )
    )

    fig.update_layout(
        title_text='Total de Movimentações vs. Total de Estadia no Porto por Mês',
        xaxis_title='Mês',
        yaxis=dict(
            title='Total de Movimentações',
            side='left',
            showgrid=False
        ),
        yaxis2=dict(
            title='Total de Estadia no Porto (Horas)',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def grafico_dif_porto_operacao(df):
    """Gráfico da diferença média entre porto e operação"""
    avg_diff_porto_operacao_mensal = df.groupby('Mês')['Diferença Porto x Operação'].mean().reset_index()

    avg_diff_porto_operacao_mensal['Mês_ordenado'] = pd.to_datetime(avg_diff_porto_operacao_mensal['Mês'], format='%m/%Y')
    avg_diff_porto_operacao_mensal = avg_diff_porto_operacao_mensal.sort_values('Mês_ordenado').drop(columns='Mês_ordenado')

    fig = px.bar(
        avg_diff_porto_operacao_mensal,
        x='Mês',
        y='Diferença Porto x Operação',
        title='Média Mensal da Diferença entre Tempo de Estadia no Porto e Tempo de Operação',
        labels={
            'Mês': 'Mês',
            'Diferença Porto x Operação': 'Média da Diferença por Cada Operação (Horas)'
        },
        hover_name='Mês'
    )

    return fig

def carregar_dados_comex(path_comex):
    """Carrega e processa os dados de comércio exterior"""
    df_comex = pd.read_excel(path_comex)
    df_comex['Mês'] = df_comex['Mês'].astype(str).str.extract(r'(\d{2})').astype(int)
    df_comex['Total_2024_Kg'] = df_comex['Exportação - 2024 - Quilograma Líquido'] + df_comex['Importação - 2024 - Quilograma Líquido']
    df_comex['FOB_2024_por_kg'] = df_comex['Exportação - 2024 - Valor US$ FOB'] / df_comex['Exportação - 2024 - Quilograma Líquido'].replace(0, np.nan)
    return df_comex

def processar_dados_navios_hipoteses(df):
    """Processa dados dos navios para as novas hipóteses"""
    df['Ano'] = df['Atracação'].dt.year
    df['Tempo_Operacao_h'] = df['Tempo de Operação H']
    df['Movs_h'] = df['Movs'] / df['Tempo_Operacao_h']
    return df

def grafico_sazonalidade_movs(df):
    """Hipótese 4 - Sazonalidade Movs por mês"""
    df_2024 = df[df['Ano'] == 2024]
    movs_mes = df_2024.groupby('Mês')['Movs'].sum().sort_index()
    
    fig = px.bar(
        x=movs_mes.index,
        y=movs_mes.values,
        title="Movs por Mês - 2024",
        labels={'x': 'Mês', 'y': 'Movs'},
        color_discrete_sequence=['seagreen']
    )
    return fig

def grafico_sazonalidade_comex(df_comex):
    """Hipótese 4 - Sazonalidade Comércio Exterior"""
    kg_mes = df_comex.groupby('Mês')['Total_2024_Kg'].sum().sort_index()
    
    fig = px.bar(
        x=kg_mes.index,
        y=kg_mes.values,
        title="Exportação + Importação por Mês - 2024",
        labels={'x': 'Mês', 'y': 'Kg'},
        color_discrete_sequence=['steelblue']
    )
    return fig

def grafico_eficiencia_servico(df):
    """Hipótese 6 - Eficiência Operacional por Serviço"""
    eficiencia = df.groupby('Serviço')['Movs_h'].mean().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=eficiencia.values,
        y=eficiencia.index,
        orientation='h',
        title="Top 10 Serviços mais Eficientes",
        labels={'x': 'Movs por Hora', 'y': 'Serviço'},
        color_discrete_sequence=['darkorange']
    )
    return fig

def grafico_produtos_municipio(df_comex):
    """Hipótese 12 - Produtos mais exportados por município"""
    produtos_mun = df_comex.groupby(['Município', 'Descrição Seção'])[
        'Exportação - 2024 - Valor US$ FOB'].sum().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=produtos_mun.values,
        y=[f"{idx[0]} - {idx[1]}" for idx in produtos_mun.index],
        orientation='h',
        title="Top 10 Produtos mais Exportados por Município (2024)",
        labels={'x': 'Valor FOB (US$)', 'y': 'Município - Produto'},
        color_discrete_sequence=['purple']
    )
    return fig

def grafico_concentracao_pais(df_comex):
    """Hipótese 14 - Concentração das Exportações por País"""
    export_pais = df_comex.groupby('País')['Exportação - 2024 - Valor US$ FOB'].sum().sort_values(ascending=False)
    total = export_pais.sum()
    pct = (export_pais / total * 100).round(2)
    
    fig = px.bar(
        x=pct.head(10).index,
        y=pct.head(10).values,
        title="Top 10 Países de Destino - % das Exportações (2024)",
        labels={'x': 'País', 'y': 'Percentual (%)'},
        color_discrete_sequence=['steelblue']
    )
    return fig, pct.head(3).sum()

def grafico_valor_fob_kg(df_comex):
    """Hipótese 15 - Produtos com Maior Valor FOB/kg"""
    valiosos = df_comex[df_comex['FOB_2024_por_kg'] > 50]
    top_valiosos = valiosos.groupby('Descrição Seção')['FOB_2024_por_kg'].mean().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=top_valiosos.values,
        y=top_valiosos.index,
        orientation='h',
        title="Top 10 Seções com Maior Valor FOB/kg (> US$ 50)",
        labels={'x': 'Valor FOB médio por kg (US$)', 'y': 'Seção'},
        color_discrete_sequence=['darkgreen']
    )
    return fig