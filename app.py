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

# Listado de Alumnos
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

# Listado de Jurado
jurado = ["Jurado 1", "Jurado 2", "Jurado 3", "Jurado 4"]

# Lista completa de personas que pueden votar
votantes_totales = jurado + alumnos

# Inicializar votos en la sesión
if 'votos' not in st.session_state:
    st.session_state.votos = pd.DataFrame(columns=['Votante', 'Proyecto', 'Nota'])

# --- SECCIÓN DE VOTACIÓN ---
with st.container():
    st.markdown('<div class="voto-card">', unsafe_allow_html=True)
    
    # Aquí aparecen Jurado + Alumnos
    persona_votando = st.selectbox("¿Quién eres?", ["Selecciona tu nombre..."] + votantes_totales)
    
    # Aquí solo aparecen Alumnos (que son los que tienen proyecto)
    proyecto_a_evaluar = st.selectbox("¿A qué proyecto de alumno vas a evaluar?", ["Selecciona proyecto..."] + alumnos)
    
    nota = st.slider("Puntuación (5 es el máximo)", 1, 5, 3)
    
    if st.button("Enviar Voto 🎥"):
        if persona_votando != "Selecciona tu nombre..." and proyecto_a_evaluar != "Selecciona proyecto...":
            if persona_votando == proyecto_a_evaluar:
                st.error("¡No puedes votarte a ti mismo! 🎅")
            else:
                nuevo_voto = pd.DataFrame({'Votante': [persona_votando], 'Proyecto': [proyecto_a_evaluar], 'Nota': [nota]})
                st.session_state.votos = pd.concat([st.session_state.votos, nuevo_voto], ignore_index=True)
                st.success(f"¡Voto de {persona_votando} registrado!")
        else:
            st.warning("Selecciona tu nombre y el proyecto antes de votar.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DEL PROFESOR Y DESCARGA ---
st.divider()
with st.expander("🔑 Panel de Control (Solo Profesor)"):
    password = st.text_input("Introduce la clave", type="password")
    
    if password == "postpro2024":
        if not st.session_state.votos.empty:
            st.subheader("🏆 Ranking Actual de Alumnos")
            # Calcula la media de cada alumno
            ranking = st.session_state.votos.groupby('Proyecto')['Nota'].mean().sort_values(ascending=False).head(3)
            for i, (nombre, media) in enumerate(ranking.items()):
                st.write(f"{i+1}º: **{nombre}** - Media: {media:.2f} ⭐")
            
            st.divider()
            
            st.subheader("📊 Exportar Datos")
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
            
            st.write("### Tabla completa de votos (incluye Jurado):")
            st.dataframe(st.session_state.votos)
        else:
            st.info("Esperando los primeros votos...")