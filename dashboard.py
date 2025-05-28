import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_excel("Dashboard_HSE_Completo.xlsx", sheet_name="Registo Diário")

# Mostra nomes das colunas para conferires
st.write("Colunas do Excel:", df.columns)

# Dashboard
st.title("Hospital Dashboard")
st.subheader("Dados reais do Excel")

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Hospitais", df["Hospital"].nunique())
col2.metric("Total de Acidentes", int(df["Nº Acidentes"].sum()))
col3.metric("Média Check-List (%)", f"{df['Check-List (%)'].mean():.1f}")
col4.metric("Total de Formações", int(df["Total Formações"].sum()))

st.markdown("---")

# Exemplo de gráfico: acidentes por hospital
fig = px.bar(
    df.groupby("Hospital")["Nº Acidentes"].sum().reset_index(),
    x="Hospital",
    y="Nº Acidentes",
    color="Hospital",
    title="Acidentes por Hospital"
)
st.plotly_chart(fig, use_container_width=True)

# Outro gráfico: evolução do Check-List (%) mês a mês
fig2 = px.line(
    df,
    x="Mês",
    y="Check-List (%)",
    color="Hospital",
    markers=True,
    title="Evolução do Check-List (%) por Hospital"
)
st.plotly_chart(fig2, use_container_width=True)