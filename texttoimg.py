import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Generador de imágenes", page_icon="🎨", layout="centered")

# Título de la aplicación
st.title("Generador de Imágenes - ingenIAr")

# Explicación
st.write("""
Esta aplicación usa tu descripción y luego usa un modelo de IngenIAr para generar una imagen a partir de esa descripción.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? ")

# Botón para ejecutar la generación de la imagen
if st.button("Generar Imagen"):
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

        # Hacer la solicitud con el prompt traducido
        with st.spinner("Generando imagen..."):
            image_bytes = query({"inputs": translated_prompt})

        # Verificar si hubo errores en la respuesta
        if image_bytes.status_code != 200:
            st.error(f"Error: {image_bytes.status_code} - {image_bytes.json().get('error', 'Unknown error')}")
        else:
            # Abrir la imagen desde la respuesta
            image = Image.open(io.BytesIO(image_bytes.content))
            
            # Mostrar la imagen en Streamlit
            st.image(image, caption="Imagen generada a partir de tu descripción", use_column_width=True)
    else:
        st.warning("Por favor, introduce un prompt para generar la imagen.")
