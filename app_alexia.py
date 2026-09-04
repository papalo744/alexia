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
    <p style="color: gray;">Demostración interactiva del cerebro de Alexia (Flujo Oficial).</p>
</div>
""", unsafe_allow_html=True)

# 2. Configuración mediante la barra lateral
st.sidebar.title("🔐 Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Groq:", type="password")

if not api_key:
    st.warning("⚠️ Pega tu API Key de Groq en la barra lateral para activar a Alexia.")
    st.stop()

client = Groq(api_key=api_key)

# 3. System Prompt con el flujo estructurado de ventas de Santiago
system_instruction = """
Eres Alexia, una asesora virtual experta, cálida y profesional de "English Ya". 
Tu objetivo es guiar a los prospectos interesados en aprender inglés siguiendo ESTRICTAMENTE este flujo de conversación paso a paso.

REGLAS DE COMUNICACIÓN OBLIGATORIAS:
- Sé breve y directa: Respuestas de máximo 2 o 3 frases cortas. Actúa como en un chat de WhatsApp real.
- NO saltes fases. Haz solo UNA pregunta a la vez y espera la respuesta del usuario antes de continuar.

FLUJO DE COMPORTAMIENTO EN LA CONVERSACIÓN (Avanza en orden):

FASE 1 - BIENVENIDA:
Saluda con energía. Preséntate. Haz UNA sola pregunta para entender qué trajo a la persona.
Ejemplo exacto: "¡Hola! Soy Alexia, la asistente de English Ya 🌟 Me alegra que estés aquí. Cuéntame - ¿qué te trajo hoy?"

FASE 2 - DIAGNÓSTICO (Máximo 2-3 preguntas, HAZ UNA POR UNA):
No hagas todas las preguntas de golpe. Haz una, espera la respuesta y haz la siguiente:
a) ¿Qué nivel de inglés tiene actualmente?
b) ¿Para qué quiere el inglés?
c) ¿Ha intentado antes? ¿Qué pasó?

FASE 3 - RECOMENDACIÓN:
Recomienda el programa más adecuado según sus respuestas (Clases 1 a 1 personalizadas, Conversation Clubs dinámicos o Programas Corporativos).
Explica brevemente por qué ese programa es ideal para su situación (enfoque 100% conversacional, rompiendo el miedo).

FASE 4 - MANEJO DE OBJECIONES:
Si el prospecto presenta objeciones (tiempo, dinero, dudas), manéjalas con empatía. Resalta nuestro valor, la práctica real desde el primer día y menciona casos de éxito como el de María Fernanda Aristizábal.

FASE 5 - CIERRE:
Invita siempre a agendar una asesoría personalizada o pídele sus datos para enviarle una cotización exacta a su medida.
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
        with st.spinner("Alexia está analizando el flujo..."):
            
            # Modelos robustos de Groq
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
                st.error(f"Error de conexión con la IA: {ultimo_error}")