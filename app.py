import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# Configuración con el Helicóptero en la pestaña
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# Muestra el dibujo del INFOCA arriba
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/1200px-Logo_del_Infoca.svg.png", width=120)
st.title("Registro de Jornadas ME-205")

# Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# --- FORMULARIO PARA ANOTAR ---
with st.form("nuevo_registro"):
    st.write("### 📝 Anotar hoy")
    
    tipo = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    jornada = st.radio("Horas jornada", [7, 8], horizontal=True)
    
    # Campo extra para el nombre del incendio/paraje
    paraje = ""
    if tipo == "Incendio":
        paraje = st.text_input("📍 ¿Dónde ha sido el incendio? (Paraje/Municipio)")
        horas_final = st.number_input("Horas totales", min_value=0.0, value=7.0, step=0.5)
    else:
        horas_final = float(jornada)
    
    submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Si hay paraje, lo añadimos al tipo (ej: "Incendio - Almonaster")
    tipo_final = f"{tipo} ({paraje})" if paraje else tipo
    
    nueva_fila = pd.DataFrame([{"Fecha": hoy, "Tipo": tipo_final, "Horas": horas_final}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    st.success(f"✅ Guardado correctamente")
    st.balloons()
    st.rerun()

st.divider()

# --- FILTRAR POR FECHAS ---
st.subheader("🔍 Filtrar por Fechas")
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Desde", value=date(2026, 1, 1))
with col2:
    fecha_fin = st.date_input("Hasta", value=datetime.now())

if not df_existente.empty:
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha']).dt.date
    mask = (df_existente['Fecha'] >= fecha_inicio) & (df_existente['Fecha'] <= fecha_fin)
    df_filtrado = df_existente.loc[mask]

    total = pd.to_numeric(df_filtrado["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES EN EL PERIODO", f"{total} h")
    
    st.write("Historial seleccionado:")
    st.table(df_filtrado.tail(15))
