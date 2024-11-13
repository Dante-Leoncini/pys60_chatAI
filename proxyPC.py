import os
from flask import Flask, request, jsonify
import requests

from huggingface_hub import InferenceClient

app = Flask(__name__)

# Asegúrate de usar tu API key de Hugging Face
API_KEY = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client = InferenceClient(api_key=API_KEY)

@app.route('/chatproxy', methods=['POST'])
def query_image():
    # Obtén el payload desde request.json
    payload = request.json
    #print("Payload recibido:", payload, flush=True)

    try:
        # Solicitar el stream del modelo (usamos stream=True para obtener una respuesta en streaming)
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.2-1B-Instruct", 
            messages=payload, 
            max_tokens=500,
            stream=True  # Cambié esto a True para recibir la respuesta en streaming
        )

        # Crear un buffer para almacenar la respuesta completa
        full_response = ""

        # Procesar el flujo de respuesta
        for chunk in stream:
            # 'choices' contiene la respuesta, 'delta' es el fragmento que llega por streaming
            if 'content' in chunk.choices[0].delta:
                # Concatenar los fragmentos de contenido
                full_response += chunk.choices[0].delta.content
                #print(chunk.choices[0].delta.content, end="")  # Opcional, para ver el progreso

        # Una vez completado el streaming, devolver la respuesta completa como JSON
        #print("Payload recibido:", payload, flush=True)
        return jsonify({"response": full_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Directorio donde se guardarán las imágenes
output_dir = "C:\\imagenes_generadas"
os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe

API_URL_IMAGE = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
@app.route('/imageproxy', methods=['POST'])
def query():
    # Obtén el payload desde request.json
    headers = {"Authorization": f'Bearer {API_KEY}'}
    payload = request.json

    try:
        response = requests.post(API_URL_IMAGE, headers=headers, json=payload)

        if response.status_code == 200:
            # Ruta del archivo donde se guardará la imagen
            image_path = os.path.join(output_dir, "generated_image.jpg")
            
            # Guardar la imagen en el disco
            with open(image_path, "wb") as f:
                f.write(response.content)
            return response.content

        else:
            print(f"Error en la solicitud a Hugging Face: {response.status_code} - {response.text}", flush=True)
            return jsonify({"error": "Error al generar la imagen"}), response.status_code

    except Exception as e:
        print(f"Excepción: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)