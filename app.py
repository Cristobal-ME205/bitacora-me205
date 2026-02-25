import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Bitácora INFOCA ME-205", layout="centered")

# Intentar cargar el logo (busca cualquier imagen que empiece por WhatsApp)
archivos = os.listdir('.')
logo_archivo = next((f for f in archivos if f.startswith('WhatsApp') and f.lower().endswith(('.png', '.jpg', '.jpeg'))), None)

if logo_archivo:
    st.image(logo_archivo, width=200)
else:
    st.title("🌲 INFOCA RETÉN ME-205")

st.subheader("Registro de Actividad Diaria")

# Formulario de entrada
with st.form("bitacora_form"):
    fecha = st.date_input("Fecha", datetime.now())
    turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
    personal = st.text_area("Personal de guardia")
    actividad = st.text_area("Descripción de la actividad / Incidencias")
    
    submitted = st.form_submit_button("Guardar Registro")

if submitted:
    nuevo_registro = {
        "Fecha": [fecha],
        "Turno": [turno],
        "Personal": [personal],
        "Actividad": [actividad]
    }
    df = pd.DataFrame(nuevo_registro)
    
    # Botón para descargar el Excel en el móvil
    st.success("✅ Registro preparado")
    
    output = pd.ExcelWriter(f"bitacora_{fecha}.xlsx", engine='xlsxwriter')
    df.to_excel(output, index=False, sheet_name='Diario')
    output.close()
    
    with open(f"bitacora_{fecha}.xlsx", "rb") as file:
        st.download_button(
            label="📥 Descargar Excel al Móvil",
            data=file,
            file_name=f"bitacora_ME205_{fecha}.xlsx",
            mime="application/vnd.ms-excel"
        )