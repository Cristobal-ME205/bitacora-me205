import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la página
st.set_page_config(page_title="INFOCA - RETÉN ME-205", layout="wide")

# 2. CABECERA PROFESIONAL (Escudo oficial y Título)
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/250px-Logo_del_Infoca.svg.png", width=120)

with col2:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="color: #1b4d2e; margin: 0; font-family: sans-serif;">INFOCA</h1>
            <p style="color: #444; margin: 0; font-size: 1.2rem; font-weight: bold;">Unidad Operativa: RETÉN ME-205</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# 3. CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE REGISTRO (Opciones ampliadas)
with st.container(border=True):
    st.markdown("### 📝 Registro de Actividad")
    c_tipo, c_jornada = st.columns(2)
    
    with c_tipo:
        # Añadidas las opciones solicitadas
        tipo_dia = st.selectbox("Clasificación de la Jornada", 
                                ["Guardia Presencial", 
                                 "Guardia No Presencial", 
                                 "Trabajos Preventivos", 
                                 "Incendio", 
                                 "Pernocta", 
                                 "Asuntos Propios", 
                                 "Vacaciones"])
    
    paraje_info = ""
    horas_totales = 7.0
    
    # Lógica específica para Incendio
    if tipo_dia == "Incendio":
        st.warning("🔥 Registro de intervención en incendio")
        paraje_info = st.text_input("📍 Ubicación / Paraje del Incendio")
        horas_totales = st.number_input("Horas de Intervención", min_value=0.0, value=7.0, step=0.5)
    else:
        with c_jornada:
            jornada_std = st.radio("Jornada Estándar (Horas)", [7, 8], horizontal=True)
            horas_totales = float(jornada_std)

    btn_guardar = st.button("REGISTRAR EN BASE DE DATOS")

# 5. LÓGICA DE GUARDADO
if btn_guardar:
    fecha_hoy = datetime.now().strftime('%d/%m/%Y')
    tipo_final = f"INCENDIO ({paraje_info})" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_fila = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": tipo_final, "Horas": horas_totales}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    
    conn.update(data=df_actualizado)
    st.success(f"Dato guardado correctamente: {tipo_final}")
    st.rerun()

st.divider()

# 6. CONSULTA DE CÓMPUTO HORARIO (Filtros Desde/Hasta)
st.markdown("### 🔍 Consulta de Cómputo Horario")
f1, f2 = st.columns(2)
with f1:
    f_desde = st.date_input("Fecha Inicio", value=date(2025, 1, 1))
with f2:
    f_hasta = st.date_input("Fecha Fin", value=datetime.now())

if not df_existente.empty:
    # Filtro de fechas para el cómputo
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'], dayfirst=True).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    # Métrica de total de horas
    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric("TOTAL HORAS PERIODO", f"{total_h} h")
    
    # Tabla de registros
    st.dataframe(df_filtro.tail(20), use_container_width=True, hide_index=True)
