import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la pestaña (El icono del navegador)
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. CABECERA PROFESIONAL INTEGRADA (Escudo Oficial + Ilustración de Extinción)
st.markdown("""
    <div style="background-color: #f4f1ea; padding: 10px; border-radius: 10px; border: 1px solid #dcdcdc; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; min-width: 300px; margin: 10px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/250px-Logo_del_Infoca.svg.png" width="100" style="margin-right: 20px;">
                <div>
                    <h1 style="color: #1e5d2b; margin: 0; font-family: sans-serif; font-size: 28px;">PLAN INFOCA</h1>
                    <p style="color: #333; margin: 0; font-weight: bold; font-size: 18px;">Registro de Jornadas ME-205</p>
                </div>
            </div>
            <div style="margin: 10px; min-width: 300px; text-align: right;">
                <svg width="350" height="120" viewBox="0 0 350 120" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                            <stop offset="0%" style="stop-color:rgb(255,200,150);stop-opacity:0.3" />
                            <stop offset="100%" style="stop-color:rgb(255,255,255);stop-opacity:0" />
                        </radialGradient>
                    </defs>
                    <rect width="350" height="120" fill="url(#grad1)" rx="10"/>
                    
                    <g transform="translate(50, 10) scale(0.8)">
                        <path d="M10,30 Q30,10 90,30 L100,50 Q80,70 20,50 Z" fill="#e74c3c"/> <rect x="30" y="5" width="60" height="5" rx="2" fill="#333"/> <rect x="0" y="35" width="15" height="15" rx="2" fill="#333"/> <path d="M40,55 Q50,90 60,110 T70,130" stroke="#3498db" stroke-width="8" stroke-linecap="round" fill="none" opacity="0.8"/>
                        <path d="M35,60 Q45,95 55,115" stroke="#a2d9ce" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.6"/>
                    </g>
                    
                    <g transform="translate(220, 20) scale(0.9)">
                        <circle cx="50" cy="20" r="15" fill="#f1c40f"/> <path d="M50,5 L50,15 M35,20 L65,20" stroke="#333" stroke-width="2"/> <rect x="30" y="35" width="40" height="50" rx="5" fill="#f1c40f"/> <rect x="35" y="85" width="30" height="40" rx="5" fill="#1e5d2b"/> <path d="M65,55 L110,40" stroke="#555" stroke-width="4" stroke-linecap="round"/> <path d="M110,40 Q130,30 150,40 T170,30" stroke="#3498db" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.7"/> </g>
                </svg>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN (La que ya tienes configurada y funciona con tu Excel)
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE ANOTACIÓN (Lógica profesional para incendios)
with st.container(border=True):
    st.markdown("### 📝 Registrar Jornada de Hoy")
    
    tipo_dia = st.selectbox("Tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    paraje_info = ""
    horas_totales = 7.0
    
    # Lógica de Incendio: Si eliges incendio, aparece el aviso y el cuadro del lugar
    if tipo_dia == "Incendio":
        st.warning("🔥 Has seleccionado INCENDIO. Por favor, indica el paraje o municipio.")
        paraje_info = st.text_input("📍 ¿Dónde ha sido el incendio? (Pueblo o Paraje)")
        horas_totales = st.number_input("Horas totales trabajadas en extinción", min_value=0.0, value=7.0, step=0.5)
    else:
        jornada_std = st.radio("Horas de jornada estándar", [7, 8], horizontal=True)
        horas_totales = float(jornada_std)
    
    btn_guardar = st.button("🚀 GUARDAR EN EL EXCEL CORPORATIVO")

# Lógica de Guardado en tu Google Sheets actual
if btn_guardar:
    fecha_hoy = datetime.now().strftime('%d/%m/%Y') # Formato de fecha día/mes/año
    # Si es incendio, guardamos el lugar junto al tipo
    texto_tipo = f"INCENDIO: {paraje_info}" if (tipo_dia == "Incendio" and paraje_info) else tipo_dia
    
    nueva_entrada = pd.DataFrame([{"Fecha": fecha_hoy, "Tipo": texto_tipo, "Horas": horas_totales}])
    
    # Unimos lo nuevo con lo existente
    df_final = pd.concat([df_existente, nueva_entrada], ignore_index=True)
    
    # Actualizamos tu hoja de cálculo
    conn.update(data=df_final)
    
    st.success(f"✅ ¡Jornada guardada correctamente!: {texto_tipo} ({horas_totales}h)")
    st.balloons()
    st.rerun()

st.divider()

# 5. FILTROS CORPORATIVOS (Desde / Hasta)
st.markdown("### 🔍 Consulta y Cómputo de Horas")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Desde el día", value=date(2025, 1, 1)) # Ajustado para empezar en 2025
with c2:
    f_hasta = st.date_input("Hasta el día", value=datetime.now())

if not df_existente.empty:
    # Ajustamos el formato de fecha para que el filtro funcione perfectamente
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha'], dayfirst=True).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtro = df_existente.loc[mask]

    # Suma de horas del periodo seleccionado
    total_h = pd.to_numeric(df_filtro["Horas"], errors='coerce').sum()
    st.metric("HORAS TOTALES ACUMULADAS", f"{total_h} h")
    
    st.write("📋 *Últimos registros en este periodo:*")
    # Mostramos los últimos 15 registros para dar más contexto
    st.table(df_filtro.tail(15))
else:
    st.info("Aún no hay registros en la base de datos.")
