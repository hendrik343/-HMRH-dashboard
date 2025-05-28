import streamlit as st
import pandas as pd
import plotly.express as px

# Liga ao ficheiro Excel verdadeiro
ficheiro_excel = "Dashboard_HSE_Completo.xlsx"
df = pd.read_excel(ficheiro_excel)

# Limpa dados vazios e ajusta colunas
df = df.dropna(subset=["Hospital"])
colunas_num = df.select_dtypes(include='number').columns.tolist()
colunas_num = [col for col in colunas_num if col != "Ano"]  # Se existir uma coluna Ano

st.title("Dashboard HSE - Comparação de Hospitais")
st.markdown("### Comparação direta de todos os indicadores")

# Mostra nomes das colunas
st.markdown("#### Dados disponíveis:")
st.write(df.head())

# Mostra gráficos para cada coluna numérica
for coluna in colunas_num:
    fig = px.bar(
        df,
        x="Hospital",
        y=coluna,
        color="Hospital",
        barmode="group",
        title=f"{coluna} por Hospital",
        text=coluna,
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Código pronto para uso • Melhorar design depois")ß