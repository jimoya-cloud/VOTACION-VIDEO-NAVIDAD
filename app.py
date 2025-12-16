import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Votación Postpo Navideña", page_icon="🎬")

# Estética Navideña y Cinematográfica con CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #d32f2f; color: white; border-radius: 10px; border: 2px solid #fbc02d; width: 100%; }
    h1 { color: #fbc02d; text-shadow: 2px 2px #d32f2f; text-align: center; }
    .voto-card { padding: 20px; border-radius: 15px; background-color: #1a1c23; border-left: 5px solid #d32f2f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Festival de Postpro Navideño 🎄")

# Lista de alumnos
alumnos = [
    "ALADREN VILLANUEVA, LUCIA", "AZNAR SERRANO, MARCOS", "BLASCO GRACIA, IVAN JORGE",
    "CARNICER IBÁÑEZ, ÁNGEL", "CARREY DENA, PABLO", "CASTILLO FERNÁNDEZ, MARTÍN",
    "CHIRAC, MARIUS DANIEL", "COLÁS PÉREZ, ÁLVARO", "DIEZ PUERTOLAS, ANDRES",
    "ESTEBAN SÁNCHEZ, VÍCTOR", "FUENTES GIMÉNEZ, EMMA", "FUSTER ZAPATER, RUBÉN",
    "GRIMA CAROD, MARTÍN", "GUERRERO GADEA, NURIA", "HERNÁNDEZ GONZÁLEZ, TANIA",
    "JIMÉNEZ DE LOS SANTOS, DIEGO", "MARÍN MARTÍN, GONZALO", "MARTÍN CASTILLO, ENZO",
    "MARTÍNEZ GRACIA, ALEJANDRO", "MONZÓN GONZÁLEZ, SARA", "ORDÓÑEZ PÉREZ, JARA",
    "PELLICER PALOMAR, MATÍAS", "PÉREZ GONZÁLEZ, RAÚL", "POKU OWUSU, MARCOS",
    "POLITE PINEDA, FRANCISCO JAVIER", "RINO BLANCO, CRISTINA", "SÁNCHEZ ROMERO, DARIO"
]

# Inicializar votos en la sesión
if 'votos' not in st.session_state:
    st.session_state.votos = pd.DataFrame(columns=['Votante', 'Proyecto', 'Nota'])

# --- SECCIÓN DE VOTACIÓN ---
with st.container():
    st.markdown('<div class="voto-card">', unsafe_allow_html=True)
    votante = st.selectbox("¿Quién eres?", ["Selecciona tu nombre..."] + alumnos)
    proyecto = st.selectbox("¿A quién vas a evaluar?", ["Selecciona proyecto..."] + alumnos)
    nota = st.slider("Puntuación (5 es el máximo)", 1, 5, 3)
    
    if st.button("Enviar Voto 🎥"):
        if votante != "Selecciona tu nombre..." and proyecto != "Selecciona proyecto...":
            if votante == proyecto:
                st.error("¡No puedes votarte a ti mismo! 🎅")
            else:
                nuevo_voto = pd.DataFrame({'Votante': [votante], 'Proyecto': [proyecto], 'Nota': [nota]})
                st.session_state.votos = pd.concat([st.session_state.votos, nuevo_voto], ignore_index=True)
                st.success(f"¡Voto enviado con éxito!")
        else:
            st.warning("Selecciona ambos nombres antes de votar.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DEL PROFESOR Y DESCARGA ---
st.divider()
with st.expander("🔑 Panel de Control (Solo Profesor)"):
    password = st.text_input("Introduce la clave", type="password")
    
    if password == "postpro2024":
        if not st.session_state.votos.empty:
            # Ranking Top 3
            st.subheader("🏆 Ranking Actual")
            ranking = st.session_state.votos.groupby('Proyecto')['Nota'].mean().sort_values(ascending=False).head(3)
            for i, (nombre, media) in enumerate(ranking.items()):
                st.write(f"{i+1}º: **{nombre}** - Media: {media:.2f} ⭐")
            
            st.divider()
            
            # Botón para descargar Excel
            st.subheader("📊 Exportar Datos")
            
            # Convertir DataFrame a Excel en memoria
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                st.session_state.votos.to_excel(writer, index=False, sheet_name='Votos')
            processed_data = output.getvalue()

            st.download_button(
                label="📥 Descargar Resultados en Excel",
                data=processed_data,
                file_name="votos_navidad_postpro.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )