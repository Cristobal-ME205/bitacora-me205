import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DEL EXCEL (TU ENLACE)
# Convertimos tu enlace normal en un enlace de descarga de datos
SHEET_ID = "1NuBt419QbI_Kws5rySiyC1ddnGWCQSciWxcrLwESOCc"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="INFOCA ME-205", layout="wide")

st.title("🌲 Registro Permanente INFOCA ME-205")

# --- FUNCIÓN PARA LEER LOS DATOS ---
def cargar_datos():
    try:
        # Lee el Excel de Google
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        # Si falla o está vacío, crea uno nuevo
        return pd.DataFrame(columns=['Fecha', 'Tipo', 'Jornada', 'Horas'])

# Cargamos el histórico
df_historico = cargar_datos()

# --- FORMULARIO DE ENTRADA ---
with st.expander("➕ REGISTRAR NUEVO DÍA", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo de Registro", ["Guardia Presencial", "Pernocta", "Incendio", "Preventivo", "Vacaciones", "Asuntos Propios"])
        jornada = st.radio("Jornada (Horas)", [7, 8], horizontal=True)
    with col2:
        fecha = st.date_input("Fecha", datetime.now())
        if tipo == "Incendio":
            horas = st.number_input("Horas totales incendio", min_value=0.0, step=0.5)
        elif tipo in ["Vacaciones", "Asuntos Propios"]:
            horas = 0.0
        else:
            horas = float(jornada)

    if st.button("💾 GUARDAR EN EL EXCEL"):
        # AQUÍ ESTÁ EL TRUCO: Te da las instrucciones para el último paso de seguridad
        st.success(f"Dato preparado: {fecha} | {tipo} | {horas}h")
        st.info("Para que se guarde físicamente, copia esta fila en tu Excel. (En el futuro lo haremos automático al 100%)")

st.divider()

# --- CÓMPUTO TOTAL (LO QUE NO SE BORRA) ---
st.subheader("📊 Cómputo Total Acumulado")
if not df_historico.empty:
    total_horas = df_historico['Horas'].sum()
    st.metric("HORAS TOTALES EN EL EXCEL", f"{total_horas} h")
    st.write("Últimos registros guardados:")
    st.dataframe(df_historico.tail(10)) # Muestra los últimos 10
else:
    st.warning("El Excel está vacío. Empieza a anotar tus días.")

st.write(f"🔗 [Abrir mi Excel para borrar o editar]({SHEET_URL.replace('/gviz/tq?tqx=out:csv', '')})")
