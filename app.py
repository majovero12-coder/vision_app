import os
import streamlit as st
import base64
from openai import OpenAI

# --- FUNCIÓN PARA ENCODEAR IMAGEN A BASE64 ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Análisis de Imagen 🤖🏞️",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    h1 {
        color: #2f3640;
        text-align: center;
        font-size: 2.6rem !important;
        font-weight: 800;
    }
    h2, h3, h4 {
        color: #353b48;
    }
    .stButton button {
        background: linear-gradient(90deg, #7f5af0, #2cb67d);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #2cb67d, #7f5af0);
    }
    .stTextInput input {
        border: 2px solid #7f5af0;
        border-radius: 10px;
    }
    .stTextArea textarea {
        border: 2px solid #9a8c98;
        border-radius: 10px !important;
    }
    .result-box {
        background-color: #f2e9e4;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 500;
        color: #22223b;
    }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.title("🤖 Análisis Inteligente de Imágenes")

st.markdown("""
Sube una imagen y deja que la IA te diga **qué ve, qué interpreta y cómo la describe** 🧠🎨  
Puedes añadir contexto adicional si quieres que el análisis sea más preciso.
""")

# --- API KEY ---
st.subheader("🔑 Autenticación")
ke = st.text_input("Introduce tu **API Key de OpenAI**:", type="password", placeholder="sk-...")

if ke:
    os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get('OPENAI_API_KEY')

# --- CLIENTE OPENAI ---
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.info("⚠️ Ingresa tu clave antes de continuar con el análisis.")

# --- SUBIDA DE IMAGEN ---
st.subheader("📸 Carga tu Imagen")
uploaded_file = st.file_uploader("Selecciona una imagen en formato JPG, PNG o JPEG", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("👀 Vista Previa de la Imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# --- CONTEXTO ADICIONAL ---
show_details = st.toggle("📝 Añadir contexto o detalles sobre la imagen")

additional_details = ""
if show_details:
    additional_details = st.text_area(
        "Describe el contexto de la imagen (opcional):",
        placeholder="Ejemplo: Esta imagen fue tomada en una exposición de arte sobre naturaleza...",
        key="details"
    )

# --- BOTÓN DE ANÁLISIS ---
analyze_button = st.button("🔍 Analizar Imagen")

# --- PROCESAMIENTO ---
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("Analizando la imagen con IA... ⏳"):
        try:
            base64_image = encode_image(uploaded_file)
            prompt_text = "Describe detalladamente lo que ves en la imagen en español."

            if show_details and additional_details:
                prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ]

            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(f"<div class='result-box'>{full_response}</div>", unsafe_allow_html=True)
            st.success("✅ Análisis completado con éxito")

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")

elif analyze_button and not uploaded_file:
    st.warning("⚠️ Por favor, sube una imagen antes de analizar.")
elif analyze_button and not api_key:
    st.warning("⚠️ Ingresa tu API Key antes de analizar.")

# --- PIE DE PÁGINA ---
st.markdown("""
---
🌟 **Desarrollado con Streamlit y OpenAI**  
Creado por *majitoo ✨*
""")

