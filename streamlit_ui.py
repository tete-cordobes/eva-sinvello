import streamlit as st
from openai_assistant import create_thread, ask_assistant
import re
from pathlib import Path

def clean_response(response):
    """
    Elimina cualquier texto que esté entre los caracteres 【 y 】, 
    independientemente de su contenido.
    """
    cleaned_response = re.sub(r'【[^】]*】', '', response)
    return cleaned_response

def run_chat_interface():
    st.set_page_config(page_title="Eva: iAsistente en Depilación", page_icon="🤖")
    
    # CSS personalizado con un indicador de escritura mejorado
    st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
        }
        .main-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 1rem;
            max-width: 600px;
            margin: 0 auto;
        }
        .logo-container {
            margin-bottom: 1rem;
        }
        .logo-container img {
            max-width: 200px;
            width: 100%;
            height: auto;
        }
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
            width: 100%;
        }
        .subtitle {
            font-size: 1rem;
            margin-bottom: 1rem;
            text-align: center;
            width: 100%;
        }
        
        /* Estilos mejorados para el indicador de escritura */
        .typing-wrapper {
            display: flex;
            align-items: center;
            padding: 8px 0;
        }
        .typing-text {
            font-size: 1rem;
            margin-right: 10px;
            color: #333;
        }
        .typing-indicator {
            display: flex;
            align-items: center;
        }
        .typing-indicator span {
            height: 8px;
            width: 8px;
            float: left;
            margin: 0 1px;
            background-color: #e91e63;
            display: block;
            border-radius: 50%;
            opacity: 0.4;
        }
        .typing-indicator span:nth-of-type(1) {
            animation: 1s blink infinite 0.3333s;
        }
        .typing-indicator span:nth-of-type(2) {
            animation: 1s blink infinite 0.6666s;
        }
        .typing-indicator span:nth-of-type(3) {
            animation: 1s blink infinite 0.9999s;
        }
        @keyframes blink {
            50% {
                opacity: 1;
            }
        }
        
        @media (min-width: 768px) {
            .title {
                font-size: 2rem;
            }
            .subtitle {
                font-size: 1.2rem;
            }
            .typing-text {
                font-size: 1.1rem;
            }
            .typing-indicator span {
                height: 10px;
                width: 10px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Contenido principal
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    # Cargar y mostrar la imagen
    image_path = Path("sinvello_logo.png")
    if image_path.exists():
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(str(image_path), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"No se pudo encontrar la imagen en: {image_path}")
    # Título centrado y en negrita
    st.markdown('<p class="title">Eva: tu iAsistente en Depilación Láser Diodo</p>', unsafe_allow_html=True)
    # Subtítulo
    st.markdown('<p class="subtitle">Pregunta lo que quieras sobre depilación láser diodo en SinVello! y Eva te contestará</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Inicializar el estado de la sesión
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = create_thread()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes del historial (ya limpios)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Procesar el input del usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí"):
        # Añadir mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Mostrar el indicador de "escribiendo" mientras se procesa la respuesta
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Mostrar el indicador de escritura animado mejorado, usando los colores de SinVello
            message_placeholder.markdown("""
                <div class="typing-wrapper">
                    <div class="typing-text">Eva está escribiendo</div>
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Obtener la respuesta del asistente
            full_response = ask_assistant(st.session_state.thread_id, prompt)
            
            # Limpiar la respuesta antes de mostrarla
            cleaned_response = clean_response(full_response)
            
            # Reemplazar el indicador de escritura con la respuesta real
            message_placeholder.markdown(cleaned_response)
        
        # Guardar la respuesta limpia en el historial
        st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
