import os
from flask import Flask, request, jsonify
import requests

import base64
import io
from datetime import datetime

from huggingface_hub import InferenceClient

app = Flask(__name__)

# Asegúrate de usar tu API key de Hugging Face
API_KEY = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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

API_URL_AUDIO = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
@app.route('/audioproxy', methods=['POST'])
def queryAudio():
    # Obtén el payload desde request.json
    headers = {"Authorization": f'Bearer {API_KEY}'}

    # Extraer el payload JSON de la solicitud
    payload = request.json
    audio_b64 = payload.get("inputs")

    if not audio_b64:
        return jsonify({"error": "No se encontró audio en la solicitud"}), 400

    #print(f"audio: {audio_b64}", flush=True)

    try:
        # Decodificar el audio en base64 a binario
        audio_data = base64.b64decode(audio_b64)
        
        # Crear la carpeta "C:/audios" si no existe
        audio_folder = "C:/audios"
        os.makedirs(audio_folder, exist_ok=True)
        
        # Generar un nombre de archivo único basado en la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join(audio_folder, f"audio_{timestamp}.wav")

        # Guardar el archivo de audio en formato WAV
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)

        print(f"Audio guardado en: {audio_path}", flush=True)        
        
        try:
            response = requests.post(API_URL_AUDIO, headers=headers, data=audio_data)

            if response.status_code == 200:
                # Ruta del archivo donde se guardará la imagen
                print(response.json().get("text"), flush=True)                

                try:
                    newQuery = '{"inputs": "'+response.json().get("text")+'"}'
                    response = requests.post(API_URL_IMAGE, headers=headers, json=newQuery)

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

            else:
                print(f"Error en la solicitud a Hugging Face: {response.status_code} - {response.text}", flush=True)
                return jsonify({"error": "Error al interpretar el audio"}), response.status_code
        
        except Exception as e:
            print(f"Excepción: {e}", flush=True)
            return jsonify({"error": str(e)}), 500

    except Exception as e:
        print(f"Error al guardar el audio: {e}", flush=True)
        return jsonify({"error": "Error al procesar el audio"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)