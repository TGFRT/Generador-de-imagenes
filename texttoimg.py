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
Esta aplicación traduce tu descripción en español al inglés, luego usa un modelo de Hugging Face para generar 4 imágenes a partir de esa descripción.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? (en español)")

# Botón para ejecutar la generación de la imagen
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

        # Crear variaciones del prompt
        prompt_variations = [
            f"{translated_prompt} in a sunny day",
            f"{translated_prompt} at sunset",
            f"{translated_prompt} with vibrant colors",
            f"{translated_prompt} in a fantasy style"
        ]

        # Generar las 4 imágenes
        images = []
        with st.spinner("Generando 4 imágenes..."):
            for i, prompt_variation in enumerate(prompt_variations):
                image_bytes = query({"inputs": prompt_variation})
                
                # Verificar si hubo errores en la respuesta
                if image_bytes.status_code == 200:
                    image = Image.open(io.BytesIO(image_bytes.content))
                    images.append(image)
                else:
                    st.error(f"Error al generar la imagen {i+1}: {image_bytes.status_code} - {image_bytes.json().get('error', 'Unknown error')}")
                    break

        # Si las 4 imágenes se generaron correctamente
        if len(images) == 4:
            # Mostrar las 4 imágenes en columnas
            cols = st.columns(4)
            for i, image in enumerate(images):
                with cols[i]:
                    st.image(image, caption=f"Imagen {i+1}")
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
        st.warning("Por favor, introduce un prompt para generar las imágenes.")
