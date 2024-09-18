import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image
import concurrent.futures
import random

# Configuración de la página
st.set_page_config(page_title="Generador de Imágenes con Traducción", page_icon="🎨", layout="centered")

# Título de la aplicación
st.title("Generador de Imágenes a partir de Descripciones en Español")

# Explicación
st.write("""
Esta aplicación traduce tu descripción en español al inglés, luego usa un modelo de Hugging Face para generar dos imágenes a partir de esa descripción.
Las imágenes serán ligeramente diferentes.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar? (en español)")

# Definir la API y los headers de Hugging Face
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

# Función para hacer la solicitud a la API de Hugging Face
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

# Botón para ejecutar la generación de las imágenes
if st.button("Generar Imágenes"):
    if user_prompt:
        # Traducir el prompt al inglés
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
        
        # Variar ligeramente el prompt para las dos imágenes añadiendo un sufijo aleatorio
        prompt_suffix_1 = f" with vibrant colors {random.randint(1, 1000)}"
        prompt_suffix_2 = f" with a dreamy atmosphere {random.randint(1, 1000)}"
        prompt_1 = translated_prompt + prompt_suffix_1
        prompt_2 = translated_prompt + prompt_suffix_2
        
        # Mostrar las traducciones al usuario (opcional, se puede eliminar si no quieres mostrar los prompts)
        # st.write(f"Prompt 1 traducido al inglés: **{prompt_1}**")
        # st.write(f"Prompt 2 traducido al inglés: **{prompt_2}**")

        # Generar las imágenes en paralelo usando concurrent.futures
        with st.spinner("Generando imágenes..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_image_1 = executor.submit(query, {"inputs": prompt_1})
                future_image_2 = executor.submit(query, {"inputs": prompt_2})
                
                # Obtener los resultados
                image_bytes_1 = future_image_1.result()
                image_bytes_2 = future_image_2.result()

        # Verificar si hubo errores en las respuestas
        if image_bytes_1.status_code != 200 or image_bytes_2.status_code != 200:
            st.error(f"Error: {image_bytes_1.status_code} - {image_bytes_1.json().get('error', 'Unknown error')}")
        else:
            # Abrir las imágenes desde las respuestas
            st.session_state.image_1 = Image.open(io.BytesIO(image_bytes_1.content))
            st.session_state.image_2 = Image.open(io.BytesIO(image_bytes_2.content))

# Si las imágenes ya se han generado, mostrarlas
if 'image_1' in st.session_state and 'image_2' in st.session_state:
    if st.session_state.image_1 and st.session_state.image_2:
        # Mostrar las imágenes en dos columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(st.session_state.image_1, caption="Imagen 1", use_column_width=True)
        
        with col2:
            st.image(st.session_state.image_2, caption="Imagen 2", use_column_width=True)

        # Crear botones de descarga para ambas imágenes
        buf1 = io.BytesIO()
        buf2 = io.BytesIO()
        st.session_state.image_1.save(buf1, format="PNG")
        st.session_state.image_2.save(buf2, format="PNG")
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
        st.warning("No se han generado imágenes. Por favor, presiona el botón de 'Generar Imágenes'.")
