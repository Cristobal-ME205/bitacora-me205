import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="INFOCA ME-205", page_icon="🌲")

# Intentar poner el logo si existe
try:
    st.image("logo.jpg", width=200)
except:
    st.title("🌲 INFOCA RETÉN ME-205")

st.markdown("### Registro de Actividad Diaria")
st.divider()

# Formulario
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha", datetime.now())
        turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
    with col2:
        personal = st.text_area("Personal de guardia")

    actividad = st.text_area("Descripción de la actividad / Incidencias", height=100)
    
    c1, c2 = st.columns(2)
    km_inicio = c1.number_input("KM Inicio", value=0)
    km_fin = c2.number_input("KM Fin", value=0)

    if st.button("🚀 Guardar Registro"):
        st.success(f"Registro guardado: {turno} - {fecha}")
        st.balloons()
