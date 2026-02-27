import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# 1. Configuración de la pestaña con el helicóptero
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

# 2. LOGO Y TÍTULO (Para que salga el dibujo sí o sí)
col_logo, col_tit = st.columns([1, 4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_del_Infoca.svg/1200px-Logo_del_Infoca.svg.png", width=120)
with col_tit:
    st.title("Registro de Jornadas ME-205")

# 3. CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)
df_existente = conn.read(ttl=0)

# 4. FORMULARIO DE ANOTACIÓN
with st.form("nuevo_registro"):
    st.subheader("📝 Anotar hoy")
    
    tipo = st.selectbox("Selecciona tipo de día", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
    
    # ESTO ES LO QUE BUSCABAS: Si eliges incendio, sale el cuadro
    paraje = ""
    if tipo == "Incendio":
        paraje = st.text_input("📍 Nombre del Incendio / Paraje", placeholder="Ej: Almonaster, Cortegana...")
        horas_incendio = st.number_input("Horas totales trabajadas", min_value=0.0, value=7.0, step=0.5)
    
    jornada_base = st.radio("Jornada estándar", [7, 8], horizontal=True)
    
    submit = st.form_submit_button("🚀 GUARDAR REGISTRO")

if submit:
    hoy = datetime.now().strftime('%Y-%m-%d')
    # Guardamos el lugar si es un incendio
    tipo_final = f"{tipo} - {paraje}" if (tipo == "Incendio" and paraje) else tipo
    valor_horas = horas_incendio if tipo == "Incendio" else float(jornada_base)
    
    nueva_fila = pd.DataFrame([{"Fecha": hoy, "Tipo": tipo_final, "Horas": valor_horas}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    st.success(f"✅ ¡Guardado! {tipo_final} ({valor_horas}h)")
    st.balloons()
    st.rerun()

st.divider()

# 5. FILTRO DE FECHAS (Las dos fechas de abajo)
st.subheader("🔍 Filtro para el Cómputo")
c1, c2 = st.columns(2)
with c1:
    f_desde = st.date_input("Desde", value=date(2026, 1, 1))
with c2:
    f_hasta = st.date_input("Hasta", value=datetime.now())

if not df_existente.empty:
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha']).dt.date
    mask = (df_existente['Fecha'] >= f_desde) & (df_existente['Fecha'] <= f_hasta)
    df_filtrado = df_existente.loc[mask]

    # CÁLCULO TOTAL
    total_h = pd.to_numeric(df_filtrado["Horas"], errors='coerce').sum()
    st.metric("TOTAL HORAS EN EL PERIODO", f"{total_h} h")
    
    st.write("### Historial:")
    st.table(df_filtrado.tail(15))
