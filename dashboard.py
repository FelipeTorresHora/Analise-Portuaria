import streamlit as st
import pandas as pd
from funcoes import *

# Configurações da página
st.set_page_config(layout="wide", page_title="Análise Portuária 2024")

# Cache para carregar os dados
@st.cache_data
def carregar_dados():
    return load_data("dados_2024_wilson.xlsx")

@st.cache_data
def carregar_dados_comex_cache():
    try:
        return carregar_dados_comex("dados_comex.xlsx")  # Ajuste o nome do arquivo
    except:
        return None
    
# Carregar os dados
df = carregar_dados()
df_comex = carregar_dados_comex_cache()
df = processar_dados_navios_hipoteses(df)

# Lista dos tópicos
topicos = ["Introdução", "Hipóteses", "Conclusão"]

# Menu lateral para selecionar o tópico
escolha = st.sidebar.radio("Navegue pelos tópicos:", topicos)

# Conteúdo que muda conforme a escolha
if escolha == "Introdução":
    st.title("Olá, seja bem-vindo à nossa análise")
    st.header("Introdução")
    st.write("""
    Este painel apresenta uma análise detalhada das operações no Porto de Salvador ao longo do ano de 2024. 
    Foram avaliadas variáveis como o tempo de estadia dos navios, tempo de operação e o volume de movimentações (Movs). 
    Buscamos compreender padrões, correlações e desvios operacionais, especialmente a partir do mês de outubro, onde foram 
    identificadas anomalias nos tempos de estadia e operação dos navios.
    
    Utilizamos gráficos para facilitar a visualização das hipóteses e aplicar técnicas de tratamento de outliers para refinar a análise. 
    O objetivo principal é entender quais fatores contribuíram para gargalos e ineficiências na operação portuária no final do ano.
    """)

elif escolha == "Hipóteses":
    st.title("Hipóteses")

    st.header("1° Hipótese:")
    st.write("O tempo de permanência dos navios no porto (desde a chegada na barra até a desatracação) está diretamente correlacionado com o volume de movimentação (Movs). Navios com mais Movs permanecem por um tempo proporcionalmente maior?")

    # Gráfico hipóteses
    fig_hip = grafico_hipoteses(df)
    st.plotly_chart(fig_hip, use_container_width=True)

    st.write("Analisando o gráfico acima, constata-se que esta hipótese é verdadeira, visto que o tempo de permanência dos navios no porto em relação à quantidade total de Movs do mês não varia muito até o mês 10/2024 (Outubro), e assim segue até 12/2024 (Dezembro), onde há um aumento muito grande no tempo de permanência sem o mesmo aumento na quantidade de Movs.")

    st.header("2° Hipótese:")
    st.write("O Tempo de Operação está diretamente correlacionado com o volume de movimentações?")

    # Reutilizar gráfico de horas x movs
    fig_hip2 = grafico_horasxmovs_mes(df)
    st.plotly_chart(fig_hip2, use_container_width=True)

    st.write("Analisando o gráfico acima, vemos que há uma correlação entre o Tempo de Operação e a quantidade de Movs, com pequenos desvios entre os meses. No entanto, a partir do mês 10 até o mês 12 temos um desvio bastante significativo, saindo do aceitável.")

    st.header("3° Hipótese: ")
    st.write("O que acontece a partir do mês 10?")

    st.write("Primeiro iremos analisar por outro ângulo, verificando a média entre a diferença de Tempo Estadia no Porto e Tempo de Operação.")

    # Gráfico diferença porto operação
    fig_dif = grafico_dif_porto_operacao(df)
    st.plotly_chart(fig_dif, use_container_width=True)

    st.write("Verifica-se que a diferença entre os meses 01/2024 e 09/2024 está entre 7 e 17 horas de atraso. Porém, a partir do mês 10 o atraso sobe consideravelmente.")

    # Causas externas adicionais
    st.subheader("Possíveis causas externas para o aumento de atraso no Porto de Salvador:")
    st.write("""
    - Greve dos Funcionários da Receita Federal iniciada em 17/10/2024, afetando diretamente a liberação de cargas e processos alfandegários.
    - Congestionamento no Porto de Santos, o principal do país, que gerou um desvio logístico de cargas para o Porto de Salvador, aumentando o fluxo e a demanda local de forma atípica.
    """)

    st.header("4° Hipótese: Sazonalidade")
    st.write("Existe um padrão de sazonalidade nas operações do porto ao longo do ano de 2024?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Movimentações por mês (Movs)**")
        fig_sazonal1 = grafico_sazonalidade_movs(df)
        st.plotly_chart(fig_sazonal1, use_container_width=True)

    with col2:
        st.markdown("**Exportações + Importações por mês (kg)**")
        fig_sazonal2 = grafico_sazonalidade_comex(df_comex)
        st.plotly_chart(fig_sazonal2, use_container_width=True)

    st.write("A análise mostra que há uma variação significativa nos volumes ao longo dos meses, indicando certa sazonalidade. Essa oscilação pode estar relacionada a fatores como calendário agrícola, demanda internacional e sazonalidade de mercado.")

    st.header("5° Hipótese: Eficiência Operacional por Serviço")
    st.write("Alguns serviços são mais eficientes em termos operacionais do que outros?")

    fig_eficiencia = grafico_eficiencia_servico(df)
    st.plotly_chart(fig_eficiencia, use_container_width=True)

    st.write("Através do gráfico, é possível observar diferenças significativas na eficiência entre os tipos de serviço. Isso pode auxiliar na tomada de decisões estratégicas sobre alocação de recursos ou melhorias operacionais específicas.")

    st.header("6° Hipótese: Exportações por Município")
    st.write("As exportações estão concentradas em determinados municípios?")

    fig_municipios = grafico_produtos_municipio(df_comex)
    st.plotly_chart(fig_municipios, use_container_width=True)

    st.write("A análise mostra uma concentração das exportações em poucos municípios, refletindo a vocação produtiva regional e as cadeias logísticas ligadas ao porto. Com isso, é possível pensar em estratégias logísticas específicas para os principais polos exportadores.")

    st.header("7° Hipótese: Concentração das Exportações por País")
    st.write("Existe concentração das exportações em poucos países de destino?")

    fig_paises, top3_pct = grafico_concentracao_pais(df_comex)
    st.plotly_chart(fig_paises, use_container_width=True)

    st.write(f"A análise revela que os três principais países de destino concentram cerca de `{top3_pct:.2f}%` das exportações totais. Isso evidencia uma dependência comercial relevante com poucos parceiros, o que pode representar riscos ou oportunidades comerciais.")

    st.header("8° Hipótese: Valor FOB por Kg")
    st.write("Quais produtos apresentam maior valor FOB (Free on Board) por quilo exportado?")

    fig_valor_fob = grafico_valor_fob_kg(df_comex)
    st.plotly_chart(fig_valor_fob, use_container_width=True)

    st.write("Os produtos com maior valor FOB por quilo são, em sua maioria, bens de alto valor agregado e menor volume. Essa análise é essencial para estratégias de rentabilidade logística, pois permite priorizar cargas com melhor relação valor/peso.")

        
elif escolha == "Conclusão":
    st.title("Conclusão")
    st.write("""
    A análise realizada sobre os dados do Porto de Salvador em 2024 revelou padrões consistentes de correlação entre o volume de movimentações e o tempo de operação dos navios, confirmando as hipóteses iniciais para a maior parte do ano.

    Entretanto, a partir de outubro observamos um aumento expressivo nos tempos de estadia, sem correspondente aumento nos Movs. Essa discrepância pode ser atribuída a fatores externos identificados, como a greve da Receita Federal iniciada em 17/10/2024 e o desvio de cargas do Porto de Santos, que enfrentava congestionamento.

    Essas anomalias reforçam a importância de análises contínuas e de considerar o contexto operacional externo. Além disso, técnicas de limpeza e tratamento de dados mostraram-se fundamentais para obter uma visão mais precisa da situação.

    Por fim, destacamos a necessidade de melhorias na infraestrutura logística e maior resiliência do sistema portuário a eventos inesperados, como greves ou mudanças repentinas no fluxo de cargas.
    """)

# Sidebar com informações adicionais
st.sidebar.markdown("---")
st.sidebar.markdown("### Informações")
st.sidebar.info("Dashboard de análise portuária desenvolvido com Streamlit")
st.sidebar.markdown(f"**Total de registros:** {len(df)}")
st.sidebar.markdown(f"**Período:** {df['Mês'].min()} a {df['Mês'].max()}")
