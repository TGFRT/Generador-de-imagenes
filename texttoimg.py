# Botón para ejecutar la generación de las imágenes
if st.button("Generar Imágenes"):
    if user_prompt:
        # Traducir el prompt al inglés
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
        
        # Variar ligeramente el prompt para las dos imágenes
        prompt_suffix_1 = f" with vibrant colors {random.randint(1, 1000)}"
        prompt_suffix_2 = f" with a dreamy atmosphere {random.randint(1, 1000)}"
        prompt_1 = translated_prompt + prompt_suffix_1
        prompt_2 = translated_prompt 
        
        # Generar las imágenes en paralelo usando concurrent.futures
        with st.spinner("Generando imágenes..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_image_1 = executor.submit(query, {"inputs": prompt_1})
                future_image_2 = executor.submit(query, {"inputs": prompt_2})
                
                image_bytes_1 = future_image_1.result()
                image_bytes_2 = future_image_2.result()

        error_messages = []

        if image_bytes_1.status_code == 429 or image_bytes_2.status_code == 429:
            error_messages.append("Error 429: Has alcanzado el límite de uso gratuito. Considera suscribirte a IngenIAr mensual y olvídate de estos límites. Podrás usar nuestras herramientas incluso sin conexión a internet.")

        if image_bytes_1.status_code != 200:
            error_message_1 = image_bytes_1.json().get('error', 'Unknown error')
            error_messages.append(f"Error al generar la Imagen 1: {error_message_1}")
            
        if image_bytes_2.status_code != 200:
            error_message_2 = image_bytes_2.json().get('error', 'Unknown error')
            error_messages.append(f"Error al generar la Imagen 2: {error_message_2}")

        # Mostrar todos los mensajes de error una sola vez
        if error_messages:
            for message in error_messages:
                st.error(message)
        else:
            st.session_state.image_1 = Image.open(io.BytesIO(image_bytes_1.content))
            st.session_state.image_2 = Image.open(io.BytesIO(image_bytes_2.content))

# Si las imágenes ya se han generado, mostrarlas
if 'image_1' in st.session_state and 'image_2' in st.session_state:
    if st.session_state.image_1 and st.session_state.image_2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(st.session_state.image_1, caption="Imagen 1", use_column_width=True)
        
        with col2:
            st.image(st.session_state.image_2, caption="Imagen 2", use_column_width=True)

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
