import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la pestaña (El icono del navegador)
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. EL LOGO (Este enlace es el del escudo oficial que buscábamos)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/250px-Logo_del_Infoca.svg.png", width=150)
st.title("Registro de Jornadas ME-205")

# 3. CONEXIÓN (Usamos la que ya tienes configurada en Streamlit)
conn = st.connection("gsheets", type=GSheetsConnection)

# Leemos los datos que ya tienes en el Excel
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE ANOTACIÓN
with st.container(border=True):
    st.subheader("📝 Anotar hoy")
    
    tipo_dia = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    paraje_info = ""
    horas_totales = 7.0
    
    # Lógica de Incendio: Si eliges incendio, aparece el cuadro del lugar
    if tipo_dia == "Incendio":
        st.info("🔥 Has seleccionado Incendio. Indica el lugar.")
        paraje_info = st.text_input("📍 ¿Dónde ha sido el incendio? (Pueblo o Paraje)")
        horas_totales = st.number_input("Horas totales trabajadas", min_value=0.0, value=7.0, step=0.5)
    else:
        jornada_std = st.radio("Jornada estándar", [7, 8], horizontal=True)
        horas_totales = float(jornada_std)
    
    btn_guardar = st.button("🚀 GUARDAR EN EL EXCEL")

# Lógica para GUARDAR en tu Excel actual
if btn_guardar:
    fecha_hoy = datetime.now().strftime('%d/%m/%Y') # Formato de fecha habitual
    # Si es incendio, guardamos el nombre del sitio al lado del tipo
    texto_tipo = f"INCENDIO ({paraje_info})" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_entrada = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": texto_tipo, "Horas": horas_totales}])
    
    # Unimos lo nuevo con lo que ya había
    df_final = pd.concat([df_existente, nueva_entrada], ignore_index=True)
    
    # Actualizamos tu Google Sheets
    conn.update(data=df_final)
    
    st.success(f"✅ ¡Guardado en tu Excel!: {texto_tipo}")
    st.balloons()
    st.rerun()

st.divider()

# 5. FILTROS (Las dos fechas de abajo para el cómputo)
st.subheader("🔍 Filtro para el Cómputo")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Desde", value=date(2024, 1, 1)) # Puesto en 2024 para que pille todo
with c2:
    f_hasta = st.date_input("Hasta", value=datetime.now())

if not df_existente.empty:
    # Convertimos la fecha para que el filtro funcione bien
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'], dayfirst=True).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    # Sumamos las horas de las filas que cumplen el filtro
    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES EN EL PERIODO", f"{total_h} h")
    
    st.write("### Historial de registros:")
    st.table(df_filtro.tail(10))
