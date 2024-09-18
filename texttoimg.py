import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image
import random

# Configuración de la página
st.set_page_config(page_title="Generador de Imágenes con Traducción", page_icon="🎨", layout="centered")

# Aplicar estilo CSS para los botones de descarga como íconos sobre las imágenes
st.markdown("""
    <style>
    /* Fondo y estilo general */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }

    /* Títulos */
    h1 {
        text-align: center;
        color: #0056b3;
    }

    /* Botón de descarga como ícono sobre la imagen */
    .download-icon {
        position: relative;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 30px;
        color: #0056b3;
    }

    .download-icon:hover {
        color: #ff6f00;
    }

    /* Imagen con borde */
    .stImage {
        border: 2px solid #0056b3;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.title("Generador de Imágenes a partir de Descripciones")

# Explicación
st.write("""
Esta aplicación traduce tu descripción en español al inglés y luego usa un modelo para generar **dos imágenes**. Introduce tu descripción y haz clic en "Generar Imágenes" para ver los resultados.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? (en español)")

# Botón para generar las imágenes
if st.button("Generar Imágenes"):
    if user_prompt:
        # Traducir el prompt al inglés
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
        
        # Variar ligeramente el prompt para las dos imágenes con un número aleatorio
        prompt_1 = translated_prompt + f" with vibrant colors {random.randint(1, 10000)}"
        prompt_2 = translated_prompt + f" with a dreamy atmosphere {random.randint(1, 10000)}"
        
        # Definir la API y los headers de Hugging Face
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": "Bearer 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"}

        # Función para hacer la solicitud a la API de Hugging Face
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response

        # Generar dos imágenes con prompts ligeramente diferentes
        with st.spinner("Generando imágenes..."):
            image_bytes_1 = query({"inputs": prompt_1})
            image_bytes_2 = query({"inputs": prompt_2})

        # Verificar si hubo errores en las respuestas
        if image_bytes_1.status_code != 200 or image_bytes_2.status_code != 200:
            st.error(f"Error: {image_bytes_1.status_code} - {image_bytes_1.json().get('error', 'Unknown error')}")
        else:
            # Abrir las imágenes desde las respuestas
            image_1 = Image.open(io.BytesIO(image_bytes_1.content))
            image_2 = Image.open(io.BytesIO(image_bytes_2.content))
            
            # Mostrar las imágenes en dos columnas
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image_1, caption="Imagen 1", use_column_width=True)
                # Crear botón de descarga como ícono sobre la imagen
                buf1 = io.BytesIO()
                image_1.save(buf1, format="PNG")
                buf1.seek(0)
                st.markdown(
                    f'<a href="data:image/png;base64,{buf1.getvalue().hex()}" download="imagen_1.png">'
                    f'<i class="download-icon">&#x2B07;</i></a>', 
                    unsafe_allow_html=True
                )
            
            with col2:
                st.image(image_2, caption="Imagen 2", use_column_width=True)
                # Crear botón de descarga como ícono sobre la imagen
                buf2 = io.BytesIO()
                image_2.save(buf2, format="PNG")
                buf2.seek(0)
                st.markdown(
                    f'<a href="data:image/png;base64,{buf2.getvalue().hex()}" download="imagen_2.png">'
                    f'<i class="download-icon">&#x2B07;</i></a>', 
                    unsafe_allow_html=True
                )
    else:
        st.warning("Por favor, introduce un prompt para generar las imágenes.")
