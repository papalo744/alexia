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

# 3. System Prompt ajustado para respuestas cortas y comerciales
system_instruction = """
Eres Alexia, una asesora virtual experta, cálida y profesional de "English Ya". 
Tu objetivo es guiar a los prospectos interesados en aprender inglés de forma rápida y persuasiva.

REGLAS DE COMUNICACIÓN OBLIGATORIAS:
- Sé breve y directa: Tus respuestas deben tener máximo 2 o 3 frases cortas. Evita los párrafos largos.
- Actúa como en un chat de WhatsApp: Mantén un ritmo ágil y dinámico.
- Cierra siempre con una pregunta sencilla para invitar al usuario a continuar la charla o a agendar su asesoría.

Información clave sobre English Ya:
- Programas: Clases 1 a 1 personalizadas, Conversation Clubs dinámicos y Capacitaciones Corporativas.
- Metodología: 100% conversacional, práctica desde el primer día y sin miedo a hablar.
- Casos de éxito: Contamos con profesionales y figuras públicas como María Fernanda Aristizábal.
- Invita siempre a agendar una asesoría para darles una cotización exacta.
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
            modelos_disponibles = [
                "openai/gpt-oss-120b",
                "llama-3.3-70b-versatile",
                "mixtral-8x7b-32768"
            ]
            
            response_text = None
            ultimo_error = None
            
            for modelo_actual in modelos_disponibles:
                try:
                    chat_completion = client.chat.completions.create(
                        model=modelo_actual,
                        messages=st.session_state.messages,
                        temperature=0.7,
                    )
                    response_text = chat_completion.choices[0].message.content
                    break
                except Exception as e:
                    ultimo_error = e
                    continue
            
            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error(f"Error en la respuesta: {ultimo_error}")
