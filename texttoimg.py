import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Generador de Imágenes con Traducción", page_icon="🎨", layout="centered")

# Título de la aplicación
st.title("Generador de Imágenes a partir de Descripciones en Español")

# Explicación
st.write("""
Esta aplicación traduce tu descripción en español al inglés, luego usa un modelo de Hugging Face para generar dos imágenes a partir de esa descripción.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? (en español)")

# Botón para ejecutar la generación de las imágenes
if st.button("Generar Imágenes"):
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

        # Generar dos imágenes con el mismo prompt traducido
        with st.spinner("Generando imágenes..."):
            image_bytes_1 = query({"inputs": translated_prompt})
            image_bytes_2 = query({"inputs": translated_prompt})

        # Verificar si hubo errores en las respuestas
        if image_bytes_1.status_code != 200 or image_bytes_2.status_code != 200:
            st.error(f"Error: {image_bytes_1.status_code} - {image_bytes_1.json().get('error', 'Unknown error')}")
        else:
            # Abrir las imágenes desde las respuestas
            image_1 = Image.open(io.BytesIO(image_bytes_1.content))
            image_2 = Image.open(io.BytesIO(image_bytes_2.content))
            
            # Mostrar las imágenes en Streamlit
            st.image([image_1, image_2], caption=["Imagen 1", "Imagen 2"], use_column_width=True)

            # Crear botones de descarga para ambas imágenes
            buf1 = io.BytesIO()
            buf2 = io.BytesIO()
            image_1.save(buf1, format="PNG")
            image_2.save(buf2, format="PNG")
            buf1.seek(0)
            buf2.seek(0)

            st.download_button(
                label="Descargar Imagen 1",
                data=buf1,
                file_name="imagen_1.png",
                mime="image/png"
            )

            st.download_button(
                label="Descargar Imagen 2",
                data=buf2,
                file_name="imagen_2.png",
                mime="image/png"
            )
    else:
        st.warning("Por favor, introduce un prompt para generar las imágenes.")
