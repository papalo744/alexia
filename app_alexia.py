import streamlit as st
from groq import Groq

# 1. Configuración de la página
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

# 2. Configuración mediante la barra lateral
st.sidebar.title("🔐 Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Groq:", type="password")

if not api_key:
    st.warning("⚠️ Pega tu API Key de Groq en la barra lateral para activar a Alexia.")
    st.stop()

client = Groq(api_key=api_key)

# 3. System Prompt y personalidad de Alexia
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

# 4. Inicializar historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# Renderizar historial en pantalla
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Caja de entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje para Alexia...", key="alexia_chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Alexia está escribiendo..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error en la respuesta: {e}")
