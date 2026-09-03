import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página de Streamlit
st.set_page_config(
    page_title="Asistente Virtual - English Ya",
    page_icon="💬",
    layout="centered"
)

st.markdown("""
<div style="text-align: center;">
    <h2>🤖 Asistente Virtual - English Ya</h2>
    <p style="color: gray;">Demostración interactiva del cerebro de Alexia.</p>
</div>
""", unsafe_allow_html=True)

# 2. Obtener la API Key de forma segura (sin quemarla en el código)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Si no hay secretos configurados, muestra un espacio seguro en la barra lateral
    st.sidebar.title("🔐 Configuración")
    api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")

if not api_key:
    st.warning("⚠️ Por favor ingresa tu API Key en la barra lateral para activar el cerebro de Alexia.")
    st.stop()

# Configurar Gemini con la llave obtenida
genai.configure(api_key=api_key)

# 3. Personalidad y conocimiento base (System Prompt de Alexia)
system_instruction = """
Eres Alexia, una asesora virtual experta, cálida, consultiva y profesional de "English Ya". 
Tu objetivo es guiar a los usuarios y prospectos interesados en aprender inglés, resolviendo sus dudas con empatía y claridad.

Información clave sobre English Ya:
- Programas disponibles: 
  1. Clases 1 a 1 (Personalizadas y adaptadas al ritmo del estudiante).
  2. Conversation Clubs (Clubes de conversación dinámicos para perder el miedo a hablar).
  3. Programas Corporativos (Capacitaciones a la medida para empresas).
- Metodología: Enfoque 100% conversacional, dinámico, enfocado en la práctica real desde el primer día, rompiendo la barrera del miedo y con profesores altamente cualificados.
- Casos de éxito destacados: Contamos con reconocidas figuras públicas y profesionales que han potenciado su carrera con nosotros, como María Fernanda Aristizábal.
- Precios y Planes: Ofrecemos diferentes paquetes flexibles según el objetivo del estudiante. Invítalos siempre a agendar una asesoría personalizada o a dejar sus datos para darles una cotización exacta a su medida.

Mantén un tono siempre amigable, persuasivo, profesional y motivador en español.
"""

# 4. Inicializar el modelo de Gemini con las instrucciones del sistema
@st.cache_resource
def load_model(key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    return model

try:
    model = load_model(api_key)
except Exception as e:
    st.error(f"Error al inicializar el modelo de IA: {e}")
    st.stop()

# 5. Inicializar el historial de conversación en la sesión de Streamlit
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 6. Renderizar el historial de mensajes en la interfaz web
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 7. Caja de entrada de chat para el usuario
if prompt := st.chat_input("Escribe tu mensaje para Alexia..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Alexia está escribiendo..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ocurrió un error al conectar con la IA: {e}")