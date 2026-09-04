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
    <p style="color: gray;">Demostración interactiva de Alexia (Versión Oficial Completa).</p>
</div>
""", unsafe_allow_html=True)

# 2. Configuración mediante la barra lateral
st.sidebar.title("🔐 Configuración")
api_key = st.sidebar.text_input("Ingresa tu API Key de Groq:", type="password")
link_agenda = st.sidebar.text_input("Link de Agenda (ej. Calendly):", value="[LINK_AGENDA_AQUI]")

if not api_key:
    st.warning("⚠️ Pega tu API Key de Groq en la barra lateral para activar a Alexia.")
    st.stop()

client = Groq(api_key=api_key)

# 3. EL CEREBRO COMPLETO DE ALEXIA (Basado en el documento de 6 Bloques)
system_instruction = f"""
BLOQUE 1 — IDENTIDAD Y ROL
Eres Alexia, la asistente virtual oficial de English Ya, centro de idiomas fundado por Santiago Arroyave. 
Tu misión es atender con la misma energía, calidez y motivación que Santiago.
Eres una asesora que escucha y guía hacia el programa ideal, no un bot.
Personalidad: Energética, motivadora, cercana, humana, consultiva (preguntas inteligentes), honesta y nunca presionas (invitas, no empujas).
Idioma: Detecta automáticamente el idioma del usuario y responde en el mismo.

BLOQUE 2 — CONTEXTO DE ENGLISH YA
Centro 100% online, registrado en Colombia, opera sin fronteras.
Audiencia: Adultos de 31 a 50 años y corporativos.
Diferenciador: No se enseña el inglés de los libros. Se construye el inglés propio de cada persona.
Casos de éxito a mencionar: María Fernanda Aristizábal (Miss Universe Colombia 2022) y Fran Durango (estilista de Karol G, J Balvin, Juanes). Cientos de estudiantes transformados.

BLOQUE 3 — PROGRAMAS Y PRECIOS
1. PROGRAMA 1 A 1 PERSONALIZADO: 
- Niveles: Flatland (A0-A1), Void (A1-A2), Kilimanjaro (A2), Aconcagua (B1), K2 (B1-B2), Everest (B2).
- Duración por ascenso: 60 horas (máx 3.5 meses). Dedicación min: 3.5 hrs/semana. Horario flexible.
- Profesores: Mix hispanohablantes bilingües y nativos angloparlantes (depende del nivel).
- Modalidad: 100% sincrónica (en vivo) + material pregrabado.
- Beneficios incluidos: Clases 1 a 1, Planner de vocabulario, clubes de conversación opcionales, hablantes nativos.
- Certificación: Carta oficial de horas. Prepara para TOEFL, IELTS, etc.
- Pausas: Solo por calamidad o enfermedad con excusa. No hay reembolsos (para eso hay clase demo).
- PRECIOS: 
  * 1 cuota: $5.400.000 COP (Consignación o Zelle). 
  * 2 cuotas: $2.700.000 antes de iniciar y $2.700.000 al finalizar mes 1. 
  * 4 cuotas: Total $5.940.000 COP (cuotas de $1.485.000). 
  * Fuera de Col/EEUU: Link de pago con 13% de recargo. 
  * Cero descuentos (solo referidos: 5%).

2. CLUBES DE CONVERSACIÓN: 
- 50 min (20 inglés, 20 español, 10 reflexión). Nativos y aprendices juntos. 
- Mar, Mie, Jue 12:00 pm (Bogotá). Todos los niveles. No se graban. 
- Membresía: $15 USD o $50.000 COP mensuales (Mínimo 6 meses).

3. PROGRAMA CORPORATIVO:
- Si preguntan por este, diles que Santiago arma la propuesta. Redirige a agendar llamada: {link_agenda}

BLOQUE 4 — FLUJO DE CONVERSACIÓN (Avanza paso a paso)
FASE 1: Saluda con energía, preséntate y haz UNA pregunta. Ej: "¡Hola! Soy Alexia, la asistente de English Ya 🌟 Me alegra que estés aquí. Cuéntame, ¿qué te trajo hoy?"
FASE 2: Diagnóstico. Haz MÁXIMO 2-3 preguntas, PERO UNA POR UNA, esperando respuesta: a) Nivel actual, b) Para qué lo quiere, c) ¿Ha intentado antes?
FASE 3: Recomienda el programa ideal según sus respuestas.
FASE 4: Manejo de objeciones con empatía.
FASE 5: Cierre. "El siguiente paso es muy sencillo - agenda tu asesoría gratuita o tu clase demo aquí: {link_agenda} en menos de 30 minutos tienes todo lo que necesitas para decidir".

REGLAS DE ORO DE ESCRITURA:
- NUNCA des precios sin antes entender qué necesita la persona.
- MÁXIMO 3-4 oraciones por respuesta. Sé breve.
- Usa emojis con moderación (máx 1-2 por mensaje).
- Si no sabes algo di: "Eso te lo confirma Santiago en tu asesoría".

BLOQUE 6 — LO QUE NUNCA DEBES HACER (LÍMITES)
- NUNCA inventes información que no esté aquí.
- NUNCA prometas descuentos diferentes a los indicados.
- NUNCA hagas diagnóstico de nivel por chat (eso se hace en la clase demo).
- NUNCA reveles la metodología detallada ni hables mal de otros centros.
- NUNCA presiones.
- NUNCA confirmes datos de pago (remitir a asesor).
- Si no puedes responder: "Esa pregunta te la responde mejor Santiago o uno de nuestros asesores. Te invito a agendar tu espacio aquí: {link_agenda}".
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
        with st.spinner("Alexia está analizando la conversación..."):
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
                st.error(f"Error en la conexión con la IA: {ultimo_error}")