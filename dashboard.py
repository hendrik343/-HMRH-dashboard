import streamlit as st
import pandas as pd
import plotly.express as px

# Título e configuração
st.set_page_config(layout="wide", page_title="Dashboard HSE - Comparação")

st.title("Dashboard HSE - Comparação de Hospitais")
st.markdown("Todos os gráficos comparam os valores totais de cada métrica para cada hospital.")

# Lê o ficheiro Excel
ficheiro_excel = "Dashboard_HSE_Completo.xlsx"
try:
    df = pd.read_excel(ficheiro_excel)
except Exception as e:
    st.error(f"Erro ao carregar o ficheiro Excel: {e}")
    st.stop()

# Garante que a coluna Hospital existe
if "Hospital" not in df.columns:
    st.error("O ficheiro não tem coluna chamada 'Hospital'. Corrija antes de continuar.")
    st.stop()

# Só mantém colunas numéricas
colunas_num = df.select_dtypes(include="number").columns.tolist()
if not colunas_num:
    st.error("Não foram encontradas colunas numéricas para comparar.")
    st.stop()

# Mostra os dados carregados
with st.expander("Ver tabela de dados"):
    st.dataframe(df)

# Um gráfico de barras para cada coluna numérica
for coluna in colunas_num:
    dados = df.groupby("Hospital")[coluna].sum().reset_index()
    fig = px.bar(
        dados,
        x="Hospital",
        y=coluna,
        color="Hospital",
        barmode="group",
        text=coluna,
        title=f"{coluna} por Hospital"
    )
    fig.update_layout(
        plot_bgcolor="#232946",
        paper_bgcolor="#232946",
        font_color="#fff",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard pronto! Todos os indicadores comparados entre hospitais.")