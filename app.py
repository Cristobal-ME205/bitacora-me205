import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración con el logo de pino en la pestaña
st.set_page_config(page_title="INFOCA ME-205", page_icon="🌲", layout="wide")

# Título con el logo
st.title("🌲 Registro Directo INFOCA ME-205")

# Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos actuales
df_existente = conn.read(ttl=0)

# --- FORMULARIO PARA ANOTAR ---
with st.form("nuevo_registro"):
    st.write("### 📝 Anotar Jornada")
    
    # Aquí tienes el selector de fecha otra vez
    fecha = st.date_input("Selecciona la fecha", datetime.now())
    
    tipo = st.selectbox("Tipo de día", [
        "Guardia Presencial", 
        "Pernocta", 
        "Incendio", 
        "Asuntos Propios", 
        "Vacaciones",
        "Refuerzo"
    ])
    
    jornada = st.radio("Horas de jornada", [7, 8], horizontal=True)
    
    # Si es incendio, te deja escribir las horas exactas
    if tipo == "Incendio":
        horas_final = st.number_input("Horas totales del incendio", min_value=0.0, value=7.0, step=0.5)
    else:
        horas_final = float(jornada)
    
    submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    # Creamos la nueva fila
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha.strftime('%d/%m/%Y'), 
        "Tipo": tipo, 
        "Horas": horas_final
    }])
    
    # Unimos y subimos
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    
    st.success(f"✅ ¡Guardado! Has anotado {horas_final}h el día {fecha.strftime('%d/%m/%Y')}")
    st.balloons()
    st.rerun()

st.divider()

# --- RESUMEN Y TOTALES ---
st.subheader("📊 Cómputo Acumulado")

if not df_existente.empty:
    # Aseguramos que la columna Horas sea numérica para sumar bien
    df_existente["Horas"] = pd.to_numeric(df_existente["Horas"], errors='coerce').fillna(0)
    total_horas = df_existente["Horas"].sum()
    
    # El total en grande
    st.metric(label="HORAS TOTALES ACUMULADAS", value=f"{total_horas} h")
    
    # Historial de los últimos 10 días
    st.write("### Últimos 10 registros")
    st.table(df_existente.tail(10))
else:
    st.info("Todavía no hay datos. ¡Empieza a anotar!")
