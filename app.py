import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Dashboard HSE - HMRH",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Generate demo data
df = gerar_dados_demo()

# Add download button
if st.sidebar.button("📥 Download Excel"):
    excel_bytes = gerar_excel(df)
    st.sidebar.download_button(
        label="📥 Download Report",
        data=excel_bytes,
        file_name=f"hse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Display data
st.title("🏥 Dashboard HSE - HMRH")
st.dataframe(df)