import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="INFOCA ME-205", layout="wide")
st.title("🌲 Registro Directo INFOCA ME-205")

# Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos actuales
df_existente = conn.read(ttl=0)

# --- FORMULARIO PARA AÑADIR ---
with st.form("nuevo_registro"):
    st.write("### 📝 Anotar Jornada")
    fecha = st.date_input("Fecha", datetime.now())
    tipo = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    jornada = st.radio("Horas de jornada", [7, 8], horizontal=True)
    horas_final = float(jornada) if tipo != "Incendio" else st.number_input("Horas del incendio", min_value=0.0, value=7.0, step=0.5)
    
    submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    nueva_fila = pd.DataFrame([{"Fecha": str(fecha), "Tipo": tipo, "Jornada": jornada, "Horas": horas_final}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    st.success("¡Guardado correctamente!")
    st.rerun()

st.divider()

# --- TOTALES ---
st.subheader("📊 Cómputo Acumulado")

if not df_existente.empty:
    # Convertir a número por si acaso
    df_existente["Horas"] = pd.to_numeric(df_existente["Horas"], errors='coerce').fillna(0)
    total = df_existente["Horas"].sum()
    
    st.metric("HORAS TOTALES", f"{total} h")
    st.write("Últimos registros guardados:")
    st.table(df_existente.tail(10))
else:
    st.info("No hay datos todavía. ¡Anota tu primera guardia!")
