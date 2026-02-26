import streamlit as st
import pandas as pd

# ENLACE DE TU EXCEL
SHEET_ID = "1NuBt419QbI_Kws5rySiyC1ddnGWCQSciWxcrLwESOCc"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="INFOCA ME-205", layout="wide")
st.title("🌲 Registro ME-205")

# Función para leer el Excel
def cargar_datos():
    try:
        df = pd.read_csv(SHEET_URL)
        # Aseguramos que la columna Horas sea número
        df['Horas'] = pd.to_numeric(df['Horas'], errors='coerce')
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

# --- AQUÍ APARECERÁ LA SUMA ---
st.subheader("📊 Resumen Acumulado")

if not df.empty:
    total_horas = df['Horas'].sum()
    st.metric("TOTAL HORAS EN EL EXCEL", f"{total_horas} h")
    
    st.write("Últimos datos anotados:")
    st.dataframe(df.tail(10))
else:
    st.error("No puedo leer los datos. Asegúrate de que el Excel tenga la columna 'Horas'.")

st.divider()
st.info("Para añadir más horas, escríbelas en tu hoja de Google Sheets y refresca esta página.")
