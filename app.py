import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la pestaña
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. DISEÑO DEL LOGO CON CÓDIGO (No se puede bloquear)
st.markdown("""
    <div style="background-color: #1e5d2b; padding: 20px; border-radius: 10px; text-align: center; border-bottom: 5px solid #f1c40f;">
        <h1 style="color: white; margin: 0; font-family: sans-serif;">🚁 INFOCA</h1>
        <p style="color: #f1c40f; margin: 0; font-weight: bold; letter-spacing: 2px;">PLAN ME-205</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Espacio en blanco

# 3. CONEXIÓN (La que ya tienes configurada y funciona)
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE ANOTACIÓN
with st.container(border=True):
    st.subheader("📝 Registrar Jornada")
    
    tipo_dia = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    paraje_info = ""
    horas_totales = 7.0
    
    # Lógica de Incendio: Aparece el cuadro para el nombre
    if tipo_dia == "Incendio":
        st.warning("🔥 Has seleccionado INCENDIO")
        paraje_info = st.text_input("📍 ¿Dónde ha sido? (Paraje / Municipio)")
        horas_totales = st.number_input("Horas totales", min_value=0.0, value=7.0, step=0.5)
    else:
        jornada_std = st.radio("Horas de jornada", [7, 8], horizontal=True)
        horas_totales = float(jornada_std)
    
    btn_guardar = st.button("🚀 GUARDAR EN MI EXCEL")

# Lógica de Guardado
if btn_guardar:
    fecha_hoy = datetime.now().strftime('%d/%m/%Y')
    texto_tipo = f"INCENDIO: {paraje_info}" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_entrada = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": texto_tipo, "Horas": horas_totales}])
    df_final = pd.concat([df_existente, nueva_entrada], ignore_index=True)
    
    conn.update(data=df_final)
    st.success(f"✅ ¡Anotado correctamente!: {texto_tipo}")
    st.balloons()
    st.rerun()

st.divider()

# 5. FILTRO PARA EL CÓMPUTO (Las dos fechas de abajo)
st.subheader("🔍 Filtro de Fechas (Cómputo)")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Desde el día", value=date(2025, 1, 1))
with c2:
    f_hasta = st.date_input("Hasta el día", value=datetime.now())

if not df_existente.empty:
    # Ajustamos las fechas para que el filtro sume bien
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'], dayfirst=True).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    # Suma de horas del periodo
    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES ACUMULADAS", f"{total_h} h")
    
    st.write("📋 *Últimos registros filtrados:*")
    st.table(df_filtro.tail(10))
