import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="INFOCA ME-205", layout="wide")
st.title("🌲 Registro Directo INFOCA ME-205")

# Conectamos con el Excel usando la llave de "Secrets"
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargamos lo que ya hay en el Excel
df_existente = conn.read(ttl=0)

# FORMULARIO PARA ESCRIBIR
with st.form("nuevo_registro"):
    st.write("### 📝 Anotar Jornada")
    fecha = st.date_input("Fecha", datetime.now())
    tipo = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    jornada = st.radio("Horas de jornada", [7, 8], horizontal=True)
    
    # Si es incendio, dejamos poner horas exactas
    if tipo == "Incendio":
        horas_final = st.number_input("Horas del incendio", min_value=0.0, value=7.0, step=0.5)
    else:
        horas_final = float(jornada)

    submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    # Creamos la nueva fila
    nueva_fila = pd.DataFrame([{"Fecha": str(fecha), "Tipo": tipo, "Jornada": jornada, "Horas": horas_final}])
    
    # Juntamos lo viejo con lo nuevo
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    
    # Lo mandamos al Excel de Google
    conn.update(data=df_actualizado)
    st.success("¡Guardado correctamente! Ya puedes ver la suma abajo.")
    st.balloons()

st.divider()

# MOSTRAR EL CÓMPUTO
st.subheader("📊 Cómputo Acumulado")
if not df_existente.empty:
    total = pd.to_numeric(df_existente["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES", f"{total} h")
    st.write("Últimos registros:")
    st.table(df_existente.tail(5))
