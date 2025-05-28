import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Dashboard HSE", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🩺 Navegação")
    secao = st.radio("Ir para:", ["Dashboard Principal", "Comparação de Métricas", "Exportar Dados"])
    st.markdown("---")
    st.markdown("**Versão:** 1.0")
    st.markdown("**Autor:** Hendrik da Silva")

# --- HEADER PERSONALIZADO ---
col1, col2 = st.columns([0.15, 0.85])
try:
    logo = Image.open("grafico_pie_acidentes.png")  # Substitua pelo seu logotipo
    col1.image(logo, width=80)
except Exception:
    col1.markdown("![Logo](https://via.placeholder.com/80)")
col2.markdown("## <span style='color:#e94560;'>Dashboard HSE</span> - Comparação entre Hospitais", unsafe_allow_html=True)
st.markdown("---")

# --- LEITURA DO FICHEIRO EXCEL ---
ficheiro_excel = "Dashboard_HSE_Completo.xlsx"
try:
    df = pd.read_excel(ficheiro_excel)
except Exception as e:
    st.error(f"Erro ao carregar o ficheiro Excel: {e}")
    st.stop()

if "Hospital" not in df.columns:
    st.error("O ficheiro não contém a coluna 'Hospital'.")
    st.stop()

df["Data"] = pd.to_datetime(df["data_formatada"], errors="coerce")
df["Mês"] = df["Data"].dt.strftime('%Y-%m')

# --- SELEÇÃO DINÂMICA DE FILTROS ---
colunas_num = df.select_dtypes(include="number").columns.tolist()
if not colunas_num:
    st.warning("Não há colunas numéricas disponíveis para visualização.")
    st.stop()

meses = sorted(df["Mês"].dropna().unique().tolist())
hospitais = df["Hospital"].unique().tolist()

with st.sidebar:
    st.markdown("### Filtros")
    hospitais_selecionados = st.multiselect("Seleciona os hospitais:", hospitais, default=hospitais)
    meses_selecionados = st.multiselect("Seleciona o(s) mês(es):", meses, default=meses[-3:])

df = df[df["Hospital"].isin(hospitais_selecionados)]
df = df[df["Mês"].isin(meses_selecionados)]

# --- SEÇÃO PRINCIPAL ---
if secao == "Dashboard Principal":
    st.subheader("📊 Indicadores Gerais por Hospital")

    with st.expander("🔍 Ver tabela de dados brutos"):
        st.dataframe(df, use_container_width=True)

    st.markdown("### 📅 Evolução Temporal dos Indicadores")
    st.markdown("Compare a performance mensal dos hospitais com base nas métricas registadas.")

    for coluna in colunas_num:
        dados = df.groupby(["Mês", "Hospital"])[coluna].sum().reset_index()
        fig = px.line(
            dados,
            x="Mês",
            y=coluna,
            color="Hospital",
            markers=True,
            title=f"Evolução mensal de {coluna}"
        )
        fig.update_layout(
            plot_bgcolor="#232946",
            paper_bgcolor="#232946",
            font_color="#ffffff",
            title_font=dict(size=20, color='#e94560'),
            xaxis_title="Mês",
            yaxis_title=coluna,
            margin=dict(t=30, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Todos os indicadores foram exibidos com sucesso.")

elif secao == "Comparação de Métricas":
    st.subheader("📈 Resumo Estatístico por Hospital")
    resumo = df.groupby("Hospital")[colunas_num].agg(["mean", "min", "max"])
    st.dataframe(resumo, use_container_width=True)

elif secao == "Exportar Dados":
    st.subheader("📤 Exportar Dados")

    def gerar_excel(dados):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dados.to_excel(writer, index=False, sheet_name='HSE')
            writer.save()
        return output.getvalue()

    excel_bytes = gerar_excel(df)

    st.download_button(
        label="📥 Descarregar Excel com dados filtrados",
        data=excel_bytes,
        file_name="dados_filtrados_HSE.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.info("Os dados incluem apenas os hospitais e meses selecionados.")

 # --- KPIs DINÂMICOS E ALERTAS ---
st.markdown("### 🚨 Alertas e Indicadores Críticos")

# Exibir a média e sinalizar valores críticos (exemplo com Acidentes e Energia)
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

# KPI 1 - Acidentes
total_acidentes = df["Acidentes"].sum() if "Acidentes" in df.columns else 0
cor_acidente = "green" if total_acidentes == 0 else "red"
kpi_col1.metric("Total de Acidentes", int(total_acidentes), delta=None, delta_color="inverse")

# KPI 2 - Energia
energia_media = df["Energia (kWh)"].mean() if "Energia (kWh)" in df.columns else 0
cor_energia = "green" if energia_media < 1000 else "orange"
kpi_col2.metric("Média de Consumo de Energia", f"{energia_media:.1f} kWh")

# KPI 3 - RSU
rsu_total = df["RSU (kg)"].sum() if "RSU (kg)" in df.columns else 0
kpi_col3.metric("Total de RSU (kg)", f"{rsu_total:.0f} kg")

# ALERTAS AUTOMÁTICOS
with st.expander("🚨 Ver Alertas Automáticos"):
    alertas = []

    if total_acidentes > 0:
        alertas.append(f"⚠️ Foram registados **{total_acidentes} acidente(s)** no(s) hospital(is) selecionado(s).")

    if energia_media > 1500:
        alertas.append(f"⚡ O consumo médio de energia está **elevado** ({energia_media:.1f} kWh).")

    if rsu_total > 5000:
        alertas.append(f"🗑️ RSU total ultrapassa o limite esperado: **{rsu_total:.0f} kg**.")

    if not alertas:
        st.success("Tudo em ordem. Nenhum alerta registado.")
    else:
        for alerta in alertas:
            st.warning(alerta)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .block-container {
        padding: 1rem 1.5rem 0rem 1.5rem;
    }
    .css-1v0mbdj, .css-1dp5vir {
        color: #e94560 !important;
    }
    .stButton > button {
        background-color: #e94560;
        color: white;
    }
</style>
""", unsafe_allow_html=True)