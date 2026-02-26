import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="INFOCA ME-205", layout="wide")

# Logo
try:
    st.image("logo.jpg", width=120)
except:
    st.title("🌲 INFOCA ME-205")

st.header("Cómputo de Jornada y Horas")
st.divider()

# --- DATOS GENERALES ---
col1, col2 = st.columns(2)

with col1:
    tipo_dia = st.selectbox("Tipo de Registro", [
        "Guardia Presencial", 
        "Guardia No Presencial",
        "Pernocta",
        "Preventivo",
        "Incendio",
        "Día por Compensación",
        "Vacaciones",
        "Asuntos Propios"
    ])
    
    # Selector de jornada manual
    jornada_base = st.radio("Jornada del día (Horas)", [7, 8], horizontal=True)

with col2:
    fecha_inicio = st.date_input("Desde el día", datetime.now())
    fecha_fin = st.date_input("Hasta el día", datetime.now())

st.divider()

# --- CÁLCULO ESPECÍFICO ---
dias_totales = (fecha_fin - fecha_inicio).days + 1
horas_calculadas = 0.0

if tipo_dia == "Incendio":
    horas_calculadas = st.number_input("Horas totales en incendio (Contabilizadas)", min_value=0.0, step=0.5)
elif tipo_dia in ["Vacaciones", "Asuntos Propios", "Día por Compensación"]:
    horas_calculadas = 0.0
    st.info(f"Día de ausencia: {dias_totales} día(s). No suma horas al cómputo.")
else:
    horas_calculadas = dias_totales * jornada_base
    st.info(f"Cálculo: {dias_totales} día(s) x {jornada_base}h")

# --- RESUMEN ---
st.subheader("Cómputo Total")
st.metric("Horas a acumular", f"{horas_calculadas} h")

if st.button("💾 Guardar Registro"):
    st.success(f"Guardado: {tipo_dia} - {horas_calculadas} horas totales.")
    st.balloons()
