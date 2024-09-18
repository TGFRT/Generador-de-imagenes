import streamlit as st
from googletrans import Translator
import requests
import io
from PIL import Image
import concurrent.futures

# Configuración de la página
st.set_page_config(page_title="Generador de Imágenes", page_icon="🎨", layout="centered")

# Título de la aplicación
st.title("Generador de Imágenes")

# Explicación
st.write("""
Esta herramienta genera imágenes de un texto, puede demorar máximo 1min, sea específico en lo que quiere generar.
""")

# Crear un objeto traductor
translator = Translator()

# Pedir al usuario el prompt en español mediante un input de Streamlit
user_prompt = st.text_input("¿Qué deseas generar?")

# Definir la API y los headers de Hugging Face
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

# Función para hacer la solicitud a la API de Hugging Face
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

# Mantener las imágenes generadas en una variable de sesión para actualizarlas cada vez que se presiona el botón
if 'image_1' not in st.session_state:
    st.session_state.image_1 = None
    st.session_state.image_2 = None

# Botón para ejecutar la generación de las imágenes
if st.button("crear"):
    if user_prompt:
        # Traducir el prompt al inglés
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
        
        # Variar ligeramente el prompt para las dos imágenes
        prompt_1 = translated_prompt + " with vibrant colors"
        prompt_2 = translated_prompt + " with a dreamy atmosphere"
        
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
