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

# 5. Caja de entrada del usuario con selector automático y reintento por respaldo
if prompt := st.chat_input("Escribe tu mensaje para Alexia...", key="alexia_chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Alexia está escribiendo..."):
            # Lista de modelos principales y de respaldo en Groq
            modelos_disponibles = [
                "llama-3.3-70b-versatile",
                "llama-3.2-3b-preview",
                "llama-3.2-1b-preview",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768"
            ]
            
            response_text = None
            ultimo_error = None
            
            # Prueba automáticamente cada modelo hasta que uno responda con éxito
            for modelo_actual in modelos_disponibles:
                try:
                    chat_completion = client.chat.completions.create(
                        model=modelo_actual,
                        messages=st.session_state.messages,
                        temperature=0.7,
                    )
                    response_text = chat_completion.choices[0].message.content
                    break # Si el modelo funciona, salimos del ciclo con éxito
                except Exception as e:
                    ultimo_error = e
                    continue # Si está obsoleto, prueba el siguiente de la lista en automático
            
            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error(f"No se pudo conectar con ningún modelo de Groq. Error: {ultimo_error}")
