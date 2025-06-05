import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Gargalos Operacionais', layout='wide')
st.title('Dashboard de Gargalos Operacionais Portuários')

st.sidebar.header('Filtros')

# Carregar dados
@st.cache_data
def load_csv(nome):
    return pd.read_csv(nome, parse_dates=True)

df_espera = load_csv('espera_barra_atracacao.csv')
df_atraso_etb = load_csv('atraso_etb_atracacao.csv')
df_permanencia = load_csv('tempo_permanencia_porto.csv')
df_concentracao = load_csv('concentracao_navios_aguardando.csv')
df_rfb = load_csv('liberacao_rfb_atrasada.csv')

aba = st.sidebar.radio('Selecione a análise:', [
    'Tempo de espera elevado (Barra x Atracação)',
    'Atrasos ETB x Atracação',
    'Permanência acima da média',
    'Concentração de navios aguardando',
    'Liberação RFB atrasada'
])

if aba == 'Tempo de espera elevado (Barra x Atracação)':
    st.subheader('Navios com tempo de espera elevado entre chegada na barra e atracação')
    st.dataframe(df_espera)
    fig = px.bar(df_espera, x='navio_/_viagem.1', y='espera_barra_atracacao', title='Tempo de Espera (h) por Navio')
    st.plotly_chart(fig, use_container_width=True)

elif aba == 'Atrasos ETB x Atracação':
    st.subheader('Atrasos entre previsão de atracação (ETB) e atracação real por berço')
    st.dataframe(df_atraso_etb)
    fig = px.bar(df_atraso_etb, x='navio_/_viagem.1', y='atraso_etb_atracacao', color='berço', title='Atraso ETB x Atracação (h)')
    st.plotly_chart(fig, use_container_width=True)

elif aba == 'Permanência acima da média':
    st.subheader('Navios com tempo de permanência acima da média no porto')
    st.dataframe(df_permanencia)
    fig = px.bar(df_permanencia, x='navio_/_viagem.1', y='tempo_porto', title='Tempo de Permanência (h) por Navio')
    st.plotly_chart(fig, use_container_width=True)

elif aba == 'Concentração de navios aguardando':
    st.subheader('Concentração de navios aguardando operação por dia')
    st.dataframe(df_concentracao)
    fig = px.line(df_concentracao, x='data', y='navios_aguardando', title='Navios aguardando operação ao longo do tempo')
    st.plotly_chart(fig, use_container_width=True)

elif aba == 'Liberação RFB atrasada':
    st.subheader('Operações com liberação da Receita Federal atrasada')
    st.dataframe(df_rfb)
    fig = px.bar(df_rfb, x='navio_/_viagem.1', y='atraso_rfb', title='Atraso Liberação RFB (h) por Navio')
    st.plotly_chart(fig, use_container_width=True)