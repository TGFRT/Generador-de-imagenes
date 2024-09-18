import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image
import random

# Configuración de la página
st.set_page_config(page_title="Generador de Imágenes con Traducción", page_icon="🎨", layout="centered")

# Título de la aplicación
st.title("Generador de Imágenes a partir de Descripciones en Español")

# Explicación
st.write("""
Esta aplicación traduce tu descripción en español al inglés, luego usa un modelo de Hugging Face para generar dos imágenes ligeramente diferentes.
Puedes hacer clic en "Volver a generar" para obtener nuevas imágenes.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? (en español)")

# Crear un botón que permitirá volver a generar las imágenes
if st.button("Generar Imágenes") or st.button("Volver a generar"):
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
            
            with col2:
                st.image(image_2, caption="Imagen 2", use_column_width=True)

            # Crear botones de descarga para ambas imágenes
            buf1 = io.BytesIO()
            buf2 = io.BytesIO()
            image_1.save(buf1, format="PNG")
            image_2.save(buf2, format="PNG")
            buf1.seek(0)
            buf2.seek(0)

            col1.download_button(
                label="Descargar Imagen 1",
                data=buf1,
                file_name="imagen_1.png",
                mime="image/png"
            )

            col2.download_button(
                label="Descargar Imagen 2",
                data=buf2,
                file_name="imagen_2.png",
                mime="image/png"
            )
    else:
        st.warning("Por favor, introduce un prompt para generar las imágenes.")
