import os
import time

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Configuração da Página
st.set_page_config(
    page_title="V-Lab Transport Dashboard", page_icon="🚛", layout="wide"
)

# Título
st.title("🚛 Monitoramento de Abastecimentos em Tempo Real")
st.markdown("---")

# Conexão com o Banco (Lê do Docker ou usa Localhost)
DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/transporte_db"
)


@st.cache_resource
def get_engine():
    return create_engine(DB_URL)


try:
    engine = get_engine()
except Exception as e:
    st.error(f"Erro de conexão: {e}")


# Função de Carga
def carregar_dados():
    try:
        query = "SELECT * FROM abastecimentos ORDER BY data_hora DESC"
        df = pd.read_sql(query, engine)
        return df
    except Exception:
        return pd.DataFrame()


# Auto-refresh
if st.button("🔄 Atualizar"):
    st.rerun()

df = carregar_dados()

if not df.empty:
    # Métricas
    col1, col2, col3 = st.columns(3)
    total = len(df)
    anomalias = df[df["improper_data"]].shape[0]
    col1.metric("Total", total)
    col2.metric("Anomalias", anomalias)

    # Tabela colorida
    def highlight_anomalia(row):
        return (
            ["background-color: #ffcccc"] * len(row)
            if row.improper_data
            else [""] * len(row)
        )

    st.dataframe(df.style.apply(highlight_anomalia, axis=1), use_container_width=True)
else:
    st.warning("Aguardando dados...")

time.sleep(5)
st.rerun()
