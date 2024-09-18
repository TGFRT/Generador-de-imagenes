import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image

# Configuración del tema
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Función para cambiar el tema
def toggle_dark_mode():
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]

# Aplicar tema oscuro o claro
if st.session_state["dark_mode"]:
    st.markdown(
        """
        <style>
        body {
            background-color: #0E0E0E;
            color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: #F0F0F0;
            color: #000000;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Título de la aplicación
st.title("🔮 Generador Tecnológico de Imágenes IA")

# Botón para cambiar el modo oscuro
st.sidebar.title("Configuraciones")
if st.sidebar.button("Cambiar a Modo Noche" if not st.session_state["dark_mode"] else "Cambiar a Modo Día"):
    toggle_dark_mode()

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
st.sidebar.write("Introduce tu descripción:")
user_prompt = st.sidebar.text_input("Descripción en español", value="Un robot futurista")

# Botón para generar o volver a generar
if st.sidebar.button("Generar Nuevas Imágenes"):
    if user_prompt:
        # Traducir el prompt al inglés
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text

        # Mostrar la traducción al usuario
        st.write(f"Prompt traducido al inglés: **{translated_prompt}**")

        # Definir la API y los headers de Hugging Face
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": "Bearer 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"}

        # Función para hacer la solicitud a la API de Hugging Face
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response

        # Crear variaciones del prompt
        prompt_variations = [
            f"{translated_prompt} in a futuristic world",
            f"{translated_prompt} with neon lights"
        ]

        # Generar las 2 imágenes
        images = []
        with st.spinner("Generando 2 imágenes..."):
            for i, prompt_variation in enumerate(prompt_variations):
                image_bytes = query({"inputs": prompt_variation})

                # Verificar si hubo errores en la respuesta
                if image_bytes.status_code == 200:
                    image = Image.open(io.BytesIO(image_bytes.content))
                    images.append(image)
                else:
                    st.error(f"Error al generar la imagen {i+1}: {image_bytes.status_code} - {image_bytes.json().get('error', 'Unknown error')}")
                    break

        # Si las 2 imágenes se generaron correctamente
        if len(images) == 2:
            # Mostrar las 2 imágenes en columnas
            cols = st.columns(2)
            for i, image in enumerate(images):
                with cols[i]:
                    st.image(image, caption=f"Imagen {i+1}", use_column_width=True)
                    # Botón para descargar cada imagen
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    st.download_button(
                        label=f"Descargar Imagen {i+1}",
                        data=img_byte_arr,
                        file_name=f"imagen_{i+1}.png",
                        mime="image/png"
                    )
    else:
        st.warning("Por favor, introduce una descripción para generar imágenes.")
else:
    st.info("Presiona 'Generar Nuevas Imágenes' para comenzar.")
