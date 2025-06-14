import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime

# Fixed Excel generation function
def gerar_excel(df):
    """Generate Excel file from dataframe"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='HSE_Data', index=False)
    output.seek(0)
    return output.getvalue()

# Demo data generation
@st.cache_data
def gerar_dados_demo():
    np.random.seed(42)
    hospitais = ["Hospital Central", "Hospital Norte", "Hospital Sul", "Hospital Leste"]
    dados = []
    for hospital in hospitais:
        for mes in range(1, 13):
            data = datetime(2024, mes, 1)
            dados.append({
                "Hospital": hospital,
                "Data": data,
                "Acidentes": np.random.poisson(2),
                "Formações": np.random.randint(10, 40),
                "Energia (kWh)": np.random.uniform(900, 1800),
                "Conformidade (%)": np.random.uniform(90, 99)
            })
    return pd.DataFrame(dados)

# CONFIGURAÇÕES INICIAIS
st.set_page_config(
    page_title="Dashboard HSE - HMRH",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add our futuristic CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(45deg, #000428 0%, #004e92 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 78, 146, 0.3);
        border: 1px solid rgba(0, 78, 146, 0.5);
        backdrop-filter: blur(10px);
    }
    
    .metrics-container {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(0, 78, 146, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
    }
    
    .alert-danger {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 65, 108, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 65, 108, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 65, 108, 0); }
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main-header">
    <h1 style="color: white;">🏥 Dashboard HSE - HMRH</h1>
    <p style="color: #88ccff;">Sistema de Monitorização de Saúde, Segurança e Ambiente</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    page = st.selectbox(
        "Select Page:",
        ["Dashboard", "Analytics", "Reports"]
    )

# Add download button in the sidebar
with st.sidebar:
    if st.button("📥 Download Excel Report"):
        df = gerar_dados_demo()  # Get your data
        excel_bytes = gerar_excel(df)
        st.download_button(
            label="📥 Download Excel",
            data=excel_bytes,
            file_name=f"hse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Main Content
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Safety Index", "98%", "2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Incidents", "5", "-2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Training Hours", "240", "15")
        st.markdown('</div>', unsafe_allow_html=True)

    # Alert Example
    st.markdown(
        '<div class="alert-danger">⚠️ Alert: 2 new safety incidents reported</div>',
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Dashboard HSE - HMRH | Version 2.0</p>
    <p>© 2024 Hendrik da Silva</p>
</div>
""", unsafe_allow_html=True)