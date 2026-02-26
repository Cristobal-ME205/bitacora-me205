import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

# Configuración con el helicóptero
st.set_page_config(page_title="INFOCA ME-205", page_icon="🚁", layout="wide")

st.title("🚁 Registro Directo INFOCA ME-205")

# Conexión con el Excel
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos actuales
df_existente = conn.read(ttl=0)

# --- FORMULARIO PARA ANOTAR ---
with st.expander("📝 ANOTAR NUEVA JORNADA", expanded=True):
    with st.form("nuevo_registro"):
        fecha_registro = st.date_input("Fecha", datetime.now())
        tipo = st.selectbox("Tipo", ["Guardia Presencial", "Pernocta", "Incendio", "Asuntos Propios", "Vacaciones"])
        jornada = st.radio("Jornada", [7, 8], horizontal=True)
        
        if tipo == "Incendio":
            horas_final = st.number_input("Horas exactas", min_value=0.0, value=7.0, step=0.5)
        else:
            horas_final = float(jornada)
        
        submit = st.form_submit_button("🚀 GUARDAR EN EL EXCEL")

if submit:
    nueva_fila = pd.DataFrame([{"Fecha": fecha_registro.strftime('%Y-%m-%d'), "Tipo": tipo, "Horas": horas_final}])
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    conn.update(data=df_actualizado)
    st.success("¡Guardado!")
    st.rerun()

st.divider()

# --- FILTRO POR FECHAS (DESDE / HASTA) ---
st.subheader("🔍 Filtrar por Fechas")
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Desde", value=date(2024, 1, 1))
with col2:
    fecha_fin = st.date_input("Hasta", value=datetime.now())

# Convertir la columna Fecha a formato fecha para poder filtrar
if not df_existente.empty:
    df_existente['Fecha'] = pd.to_datetime(df_existente['Fecha']).dt.date
    
    # Filtrar los datos según las fechas elegidas
    mask = (df_existente['Fecha'] >= fecha_inicio) & (df_existente['Fecha'] <= fecha_fin)
    df_filtrado = df_existente.loc[mask]

    # --- TOTALES FILTRADOS ---
    st.subheader(f"📊 Cómputo del periodo seleccionado")
    total_filtrado = pd.to_numeric(df_filtrado["Horas"], errors='coerce').sum()
    st.metric("HORAS EN ESTE PERIODO", f"{total_filtrado} h")
    
    st.write("Registros encontrados:")
    st.table(df_filtrado)
else:
    st.info("Aún no hay datos guardados.")
