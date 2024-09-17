pip install googletrans==4.0.0-rc1
from googletrans import Translator

# Crear un traductor
translator = Translator()

# Pedir al usuario el prompt en español
user_prompt = input("¿Qué deseas generar? : ")

# Traducir el prompt al inglés
translated_prompt = translator.translate(user_prompt, src='es', dest='en').text

# Guardar la traducción en una variable
translation = translated_prompt

import requests
import io
from PIL import Image
import matplotlib.pyplot as plt

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

image_bytes = query({
    "inputs": translation,
})

# Check for errors in the response
if image_bytes.status_code != 200: # Check if the request was successful
    print(f"Error: {image_bytes.status_code} - {image_bytes.json()['error']}") # Print the error message
else:
    image = Image.open(io.BytesIO(image_bytes.content)) # Open the image if the request was successful
    plt.imshow(image)
    plt.axis('off')
    plt.show()
