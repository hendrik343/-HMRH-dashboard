import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

with st.sidebar:
    st.title("🩺 Navegação")
    st.markdown("- Dashboard Principal")
    st.markdown("- Comparação de Métricas")
    st.markdown("- Exportar Dados")
    st.markdown("---")
    st.markdown("Versão 1.0")

# Header personalizado com logo
col1, col2 = st.columns([0.15, 0.85])
logo = Image.open("grafico_pie_acidentes.png")  # Substituir pelo logo da empresa
col1.image(logo, width=80)
col2.markdown("## <span style='color:#e94560;'>Dashboard HSE</span> - Comparação de Hospitais", unsafe_allow_html=True)
st.markdown("---")

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

hospitais = df["Hospital"].unique().tolist()
hospitais_selecionados = st.multiselect("Seleciona os hospitais:", hospitais, default=hospitais)

df = df[df["Hospital"].isin(hospitais_selecionados)]

# Mostra os dados carregados
with st.expander("Ver tabela de dados"):
    st.dataframe(df)

# Um gráfico de barras para cada coluna numérica
for coluna in colunas_num:
    dados = df.groupby("Hospital")[coluna].sum().reset_index()
    is_horizontal = coluna in ["RSU (kg)", "Energia (kWh)", "Água (m³)", "Combustível (L)"]
    chart_type = px.bar if not is_horizontal else px.bar
    orientation = "v" if not is_horizontal else "h"
    eixo_x = "Hospital" if not is_horizontal else coluna
    eixo_y = coluna if not is_horizontal else "Hospital"

    fig = chart_type(
        dados,
        x=eixo_x,
        y=eixo_y,
        orientation=orientation,
        color="Hospital",
        text=coluna,
        title=f"{coluna} por Hospital"
    )
    fig.update_layout(
        plot_bgcolor="#232946",
        paper_bgcolor="#232946",
        font_color="#ffffff",
        title={
            'text': f"{coluna} por Hospital",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=22, color='#e94560')
        },
        margin=dict(t=30, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard pronto! Todos os indicadores comparados entre hospitais.")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)