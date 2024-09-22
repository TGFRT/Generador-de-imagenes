if st.button("Generar Imágenes"):
    if user_prompt:
        translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
        
        prompt_suffix_1 = f" with vibrant colors {random.randint(1, 1000)}"
        prompt_suffix_2 = f" with a dreamy atmosphere {random.randint(1, 1000)}"
        prompt_1 = translated_prompt + prompt_suffix_1
        prompt_2 = translated_prompt 
        
        with st.spinner("Generando imágenes..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_image_1 = executor.submit(query, {"inputs": prompt_1})
                future_image_2 = executor.submit(query, {"inputs": prompt_2})
                
                image_bytes_1 = future_image_1.result()
                image_bytes_2 = future_image_2.result()

        error_occurred = False
        
        if image_bytes_1.status_code == 429:
            st.error("Error 429: Has alcanzado el límite de uso gratuito. Considera suscribirte a IngenIAr mensual y olvídate de estos límites. Podrás usar nuestras herramientas incluso sin conexión a internet.")
            error_occurred = True
        elif image_bytes_1.status_code != 200:
            error_message_1 = image_bytes_1.json().get('error', 'Unknown error')
            st.error(f"Error al generar la Imagen 1: {error_message_1}")
            error_occurred = True
            
        if image_bytes_2.status_code == 429:
            st.error("Error 429: Has alcanzado el límite de uso gratuito. Considera suscribirte a IngenIAr mensual y olvídate de estos límites. Podrás usar nuestras herramientas incluso sin conexión a internet.")
            error_occurred = True
        elif image_bytes_2.status_code != 200:
            error_message_2 = image_bytes_2.json().get('error', 'Unknown error')
            st.error(f"Error al generar la Imagen 2: {error_message_2}")
            error_occurred = True
            
        if not error_occurred:
            st.session_state.image_1 = Image.open(io.BytesIO(image_bytes_1.content))
            st.session_state.image_2 = Image.open(io.BytesIO(image_bytes_2.content))
