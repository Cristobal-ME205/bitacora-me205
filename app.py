import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración con el Helicóptero
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. Logo oficial del INFOCA (como en el video)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/1200px-Logo_del_Infoca.svg.png", width=120)
st.title("Registro de Jornadas ME-205")

# 3. Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# --- FORMULARIO PARA ANOTAR ---
with st.form("nuevo_registro"):
    st.write("### 📝 Anotar hoy")
    # He quitado el selector de fecha de aquí para que NO salgan tres. 
    # Por defecto, se guardará con la fecha de hoy.
    tipo = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    jornada = st.radio("Horas jornada", [7, 8], horizontal=True)
    
    if tipo == "Incendio":
        horas_final = st.number_input("Horas incendio", min_value=0.0, value=7.0, step=0.5)
    else:
        horas_final = float(jornada)
    
    submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    # Registra automáticamente con la fecha de hoy
    hoy = datetime.now().strftime('%Y-%m-%d')
    nueva_fila = pd.DataFrame([{"Fecha": hoy, "Tipo": tipo, "Horas": horas_final}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    st.success(f"¡Guardado hoy {hoy}!")
    st.balloons()
    st.rerun()

st.divider()

# --- FILTRAR POR FECHAS (Aquí están las dos que necesitas) ---
st.subheader("🔍 Filtrar por Fechas")
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Desde", value=date(2024, 1, 1))
with col2:
    fecha_fin = st.date_input("Hasta", value=datetime.now())

if not df_existente.empty:
    # Convertimos para que el filtro funcione
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha']).dt.date
    mask = (df_existente['Fecha'] >= fecha_inicio) & (df_existente['Fecha'] <= fecha_fin)
    df_filtrado = df_existente.loc[mask]

    # --- TOTALES ---
    total = pd.to_numeric(df_filtrado["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES", f"{total} h")
    
    st.write("Detalle de las jornadas:")
    st.table(df_filtrado.tail(10))
