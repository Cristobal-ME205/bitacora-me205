import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la pestaña
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. EL LOGO (Ahora usando el enlace oficial directo)
st.image("https://www.agenciamedioambienteyagua.es/images/logo_infoca.png", width=200)
st.title("Registro de Jornadas ME-205")

# 3. CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE ANOTACIÓN
with st.container(border=True):
    st.subheader("📝 Anotar hoy")
    
    tipo_dia = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    paraje_info = ""
    horas_totales = 7.0
    
    # Si eliges incendio, sale el cuadro del lugar
    if tipo_dia == "Incendio":
        st.info("🔥 Has seleccionado Incendio. Por favor, indica el lugar.")
        paraje_info = st.text_input("📍 ¿Dónde ha sido el incendio? (Pueblo o Paraje)")
        horas_totales = st.number_input("Horas totales trabajadas", min_value=0.0, value=7.0, step=0.5)
    else:
        jornada_std = st.radio("Jornada estándar", [7, 8], horizontal=True)
        horas_totales = float(jornada_std)
    
    btn_guardar = st.button("🚀 GUARDAR EN EL EXCEL")

if btn_guardar:
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    texto_tipo = f"INCENDIO: {paraje_info}" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_entrada = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": texto_tipo, "Horas": horas_totales}])
    df_final = pd.concat([df_existente, nueva_entrada], ignore_index=True)
    conn.update(data=df_final)
    st.success(f"✅ Registrado correctamente")
    st.balloons()
    st.rerun()

st.divider()

# 5. FILTROS (Tus dos fechas de abajo)
st.subheader("🔍 Filtro para el Cómputo")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Desde", value=date(2026, 1, 1))
with c2:
    f_hasta = st.date_input("Hasta", value=datetime.now())

if not df_existente.empty:
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha']).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES", f"{total_h} h")
    st.table(df_filtro.tail(10))
