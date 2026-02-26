import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Cómputo Horario ME-205", layout="wide")

# Título y Logo
try:
    st.image("logo.jpg", width=150)
except:
    st.title("🌲 INFOCA ME-205")

st.header("Control de Jornada y Horas")
st.divider()

# --- SECCIÓN 1: DATOS DE LA JORNADA ---
col1, col2 = st.columns(2)

with col1:
    tipo_dia = st.selectbox("Tipo de Jornada / Ausencia", [
        "Guardia Presencial", 
        "Guardia No Presencial (Disponibilidad)",
        "Pernocta",
        "Preventivo",
        "Incendio",
        "Día por Compensación",
        "Vacaciones",
        "Asuntos Propios"
    ])
    
    fecha_inicio = st.date_input("Fecha Inicio", datetime.now())
    fecha_fin = st.date_input("Fecha Fin", datetime.now())

with col2:
    # Lógica de horas según el mes (7h u 8h)
    mes_actual = fecha_inicio.month
    # Supongamos: Meses de verano (6,7,8,9) son 8h, el resto 7h (Ajusta si es distinto)
    horas_base = 8 if mes_actual in [6, 7, 8, 9] else 7
    st.info(f"Jornada base para este mes: {horas_base} horas")
    
    if tipo_dia == "Incendio":
        horas_incendio = st.number_input("Cantidad de horas en Incendio", min_value=0.0, step=0.5)
    else:
        st.write("Jornada estándar aplicada")

# --- SECCIÓN 2: CÓMPUTO ---
st.subheader("Resumen del Registro")
dias_totales = (fecha_fin - fecha_inicio).days + 1

if tipo_dia == "Incendio":
    total_horas = horas_incendio
elif tipo_dia in ["Vacaciones", "Asuntos Propios", "Día por Compensación"]:
    total_horas = 0
else:
    total_horas = dias_totales * horas_base

st.metric("Total Horas para el Cómputo", f"{total_horas} h")

# --- BOTÓN GUARDAR ---
if st.button("💾 Guardar en el Histórico"):
    st.success(f"Registrado: {tipo_dia} ({dias_totales} días). Total: {total_horas} horas.")
    st.balloons()
