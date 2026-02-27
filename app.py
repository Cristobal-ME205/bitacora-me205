import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración técnica de la página
st.set_page_config(page_title="INFOCA - RETÉN ME-205", layout="wide")

# 2. CABECERA CORPORATIVA (Diseño Profesional)
st.markdown("""
    <div style="background-color: #1b4d2e; padding: 20px; border-radius: 5px; display: flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/250px-Logo_del_Infoca.svg.png" width="80" style="margin-right: 20px;">
        <div>
            <h1 style="color: white; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; letter-spacing: 1px;">INFOCA</h1>
            <p style="color: #cbd5e0; margin: 0; font-size: 1.1rem; font-weight: 500;">Unidad Operativa: RETÉN ME-205</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("") 

# 3. CONEXIÓN A LA BASE DE DATOS (Google Sheets)
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. ÁREA DE REGISTRO TÉCNICO
with st.form("registro_jornada"):
    st.markdown("### 📝 Registro de Actividad")
    col_a, col_b = st.columns(2)
    
    with col_a:
        tipo_dia = st.selectbox("Clasificación de la Jornada", 
                                ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    with col_b:
        # Lógica de Incendio integrada
        if tipo_dia == "Incendio":
            paraje_info = st.text_input("📍 Ubicación / Paraje del Incendio", placeholder="Ej: Sierra de Aracena")
            horas_totales = st.number_input("Horas de Intervención", min_value=0.0, value=7.0, step=0.5)
        else:
            jornada_std = st.radio("Jornada Estándar (Horas)", [7, 8], horizontal=True)
            horas_totales = float(jornada_std)
            paraje_info = ""

    submit = st.form_submit_button("REGISTRAR EN BASE DE DATOS")

# Procesamiento de Guardado
if submit:
    fecha_hoy = datetime.now().strftime('%d/%m/%Y')
    # Guardamos de forma técnica: INCENDIO (Lugar) o el tipo normal
    tipo_final = f"INCENDIO ({paraje_info})" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_fila = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": tipo_final, "Horas": horas_totales}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    
    conn.update(data=df_actualizado)
    st.success(f"Dato procesado correctamente: {tipo_final}")
    st.rerun()

st.divider()

# 5. PANEL DE CONTROL Y CÓMPUTO
st.markdown("### 🔍 Consulta de Cómputo Horario")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Fecha Inicio Periodo", value=date(2025, 1, 1))
with c2:
    f_hasta = st.date_input("Fecha Fin Periodo", value=datetime.now())

if not df_existente.empty:
    # Filtro dinámico de fechas
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'], dayfirst=True).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    # Métrica profesional
    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric(label="SUMATORIO HORAS PERIODO", value=f"{total_h} h")
    
    st.markdown("#### Historial Reciente")
    st.dataframe(df_filtro.tail(20), use_container_width=True, hide_index=True)
