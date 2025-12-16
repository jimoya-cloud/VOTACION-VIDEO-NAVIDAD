import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Votación Postpo Navideña", page_icon="🎬")

# Estética Navideña y Cinematográfica con CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #d32f2f;
        color: white;
        border-radius: 10px;
        border: 2px solid #fbc02d;
    }
    h1 {
        color: #fbc02d;
        text-shadow: 2px 2px #d32f2f;
        text-align: center;
    }
    .voto-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1a1c23;
        border-left: 5px solid #d32f2f;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título y encabezado
st.title("🎬 Festival de Postpro Navideño 🎄")
st.write("Selecciona tu nombre, el compañero al que evalúas y dale tu puntuación (1-5).")

# Lista de alumnos cargada de tu archivo
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

# Inicializar base de datos temporal (En producción usar st.connection)
if 'votos' not in st.session_state:
    st.session_state.votos = pd.DataFrame(columns=['Votante', 'Proyecto', 'Nota'])

# --- INTERFAZ DE VOTACIÓN ---
with st.container():
    st.markdown('<div class="voto-card">', unsafe_allow_html=True)
    votante = st.selectbox("¿Quién eres?", ["Selecciona tu nombre..."] + alumnos)
    proyecto = st.selectbox("¿A qué compañero vas a evaluar?", ["Selecciona proyecto..."] + alumnos)
    nota = st.slider("Puntuación (5 es el máximo)", 1, 5, 3)
    
    if st.button("Enviar Voto 🎥"):
        if votante != "Selecciona tu nombre..." and proyecto != "Selecciona proyecto...":
            if votante == proyecto:
                st.error("¡No puedes votarte a ti mismo, tramposillo! 🎅")
            else:
                nuevo_voto = pd.DataFrame({'Votante': [votante], 'Proyecto': [proyecto], 'Nota': [nota]})
                st.session_state.votos = pd.concat([st.session_state.votos, nuevo_voto], ignore_index=True)
                st.success(f"Voto registrado para el proyecto de {proyecto}. ¡Gracias!")
        else:
            st.warning("Por favor, selecciona ambos nombres.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DEL PROFESOR (RANKING) ---
st.divider()
with st.expander("🔑 Panel de Control (Solo Profesor)"):
    password = st.text_input("Introduce la clave", type="password")
    if password == "postpro2024":
        st.subheader("🏆 Top 3 Proyectos")
        if not st.session_state.votos.empty:
            ranking = st.session_state.votos.groupby('Proyecto')['Nota'].mean().sort_values(ascending=False).head(3)
            for i, (nombre, media) in enumerate(ranking.items()):
                st.write(f"🥇 Posición {i+1}: **{nombre}** con una media de **{media:.2f}**")
            
            st.write("### Detalle de votos totales")
            st.dataframe(st.session_state.votos)
        else:
            st.info("Aún no hay votos registrados.")