# -*- coding: utf-8 -*-
import httplib
import appuifw
import e32
import audio
import graphics
import os
import base64

canvas = appuifw.Canvas()
appuifw.app.body = canvas
canvas.clear(0xEEEEEE)  # Limpiar el canvas
texto = u"Graba y Envia un audio para generar la imagen"
canvas.text((10, 20), texto, fill=0x000000, font="dense")  # Dibujar el texto

proxy_url = '192.168.0.59:5000'  # Reemplaza con la IP y puerto de tu proxy
path = '/audioproxy'

headers = {
    'Content-Type': 'application/json'
}

audio_path = "E:\\recorded_audio.wav"  # Ruta donde se guardará el audio

# Texto a mostrar

def dibujartiempo(tiempo):
    canvas.clear(0xEEEEEE)  # Limpiar el canvas
    texto = u"grabando: quedan "+str(tiempo)+" segundos"
    canvas.text((10, 20), texto, fill=0x000000, font="dense")  # Dibujar el texto
    e32.ao_sleep(1)

# Función para grabar el audio
def record_audio():
    global audio_path

    # Verificar si el archivo ya existe y eliminarlo
    if os.path.exists(audio_path):
        os.remove(audio_path)
        
    rec = audio.Sound.open(audio_path)
    rec.record()  # Iniciar grabación

    dibujartiempo(5)
    dibujartiempo(4)
    dibujartiempo(3)
    dibujartiempo(2)
    dibujartiempo(1)

    canvas.clear(0xEEEEEE)  # Limpiar el canvas
    texto = u"Envie el audio para generar la imagen"
    canvas.text((10, 20), texto, fill=0x000000, font="dense")  # Dibujar el texto

    rec.stop()  # Detener grabación
    rec.close()
    appuifw.note(u"Grabación completada", "conf")

def ver_imagen():     
    image_path = "E:\\generated_image.jpg"   
    # Cargar y dibujar la imagen en el Canvas
    img = graphics.Image.open(image_path)
    img_resized = img.resize((240, 240))
    # Dibujar la imagen redimensionada en el Canvas
    canvas.clear(0x000000)  # Limpiar el canvas
    canvas.blit(img_resized, target=(0, 0))

# Función para enviar el audio grabado
def send_audio():
    try:
        # Abrir el archivo de audio en modo binario y leer su contenido
        f = open(audio_path, "rb")
        try:
            audio_data = base64.b64encode(f.read()).decode('utf-8')
        finally:
            f.close()
        
        # Crear el cuerpo JSON con el audio codificado
        json_data = '{"inputs": "' + audio_data + '"}'

        # Realizar la conexión HTTP con el servidor
        conn = httplib.HTTPConnection(proxy_url)
        conn.request("POST", path, body=json_data, headers=headers)
        
        response = conn.getresponse()
        if response.status != 200:
            print("Error: Respuesta no exitosa del servidor:", response.status)
            return
        
        # Leer la respuesta en binario directamente
        image_data = response.read()
        conn.close()
        
        print("Tamaño de image_data recibido:", len(image_data))
        
        # Guardar la imagen temporalmente en el dispositivo
        image_path = "E:\\generated_image.jpg"
        
        # Asegúrate de abrir el archivo en modo binario
        f = open(image_path, "wb")
        try:
            f.write(image_data)
        finally:
            f.close()

        print("Imagen guardada en:", image_path)
        ver_imagen()

    except Exception:
        print("Error al conectar con la API o procesar el audio")

# Menú simple
appuifw.app.menu = [
    (u"Grabar audio", record_audio),
    (u"Audio a Imagen", send_audio),
    (u"Ver Imagen Guarda", ver_imagen)
]

# Mantener la aplicación corriendo hasta que se cierre
def salir():
    app_lock.signal()

appuifw.app.exit_key_handler = salir
app_lock = e32.Ao_lock()
app_lock.wait()