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

# Variable para controlar la grabación
is_recording = False

def dibujartiempo(tiempo):
    canvas.clear(0xEEEEEE)  # Limpiar el canvas
    texto = u"Grabando: han transcurrido " + str(tiempo) + " segundos"
    canvas.text((10, 20), texto, fill=0x000000, font="dense")  # Dibujar el texto

def stop_recording():
    global is_recording
    is_recording = False
    update_menu()

def start_recording():
    global is_recording
    is_recording = True
    update_menu()
    record_audio()

# Función para grabar el audio
def record_audio():
    global audio_path, is_recording

    # Verificar si el archivo ya existe y eliminarlo
    if os.path.exists(audio_path):
        os.remove(audio_path)

    rec = audio.Sound.open(audio_path)
    rec.record()  # Iniciar grabación

    tiempo_transcurrido = 0

    # Actualizar el canvas con el tiempo transcurrido mientras se graba
    while is_recording:
        dibujartiempo(tiempo_transcurrido)
        e32.ao_sleep(1)  # Pausa de 1 segundo
        tiempo_transcurrido += 1

    # Detener la grabación
    rec.stop()
    rec.close()

    canvas.clear(0xEEEEEE)  # Limpiar el canvas
    texto = u"Procesando..."
    canvas.text((10, 20), texto, fill=0x000000, font="dense")  # Dibujar el texto
    send_audio()

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
        update_menu()

    except Exception:
        update_menu()
        print("Error al conectar con la API o procesar el audio")

def update_menu():
    #Actualizar el menú dependiendo del estado de la grabación.
    if is_recording:
        appuifw.app.menu = [
            (u"Detener grabación", stop_recording)
        ]
    else:
        appuifw.app.menu = [
            (u"Grabar audio", start_recording)
        ]
        #(u"Audio a Imagen", send_audio)

"""def update_left_button():
    #Actualizar la función del botón izquierdo (menú) dependiendo del estado de la grabación.
    if is_recording:
        appuifw.app.left_softkey = (u"Detener grabación", stop_recording)
    else:
        appuifw.app.left_softkey = (u"Grabar audio", start_recording)"""

# Inicializar el menú
update_menu()

# Mantener la aplicación corriendo hasta que se cierre
def salir():
    stop_recording()
    app_lock.signal()

# Configurar el botón derecho para cerrar la aplicación
appuifw.app.exit_key_handler = salir

# Configurar el botón izquierdo para iniciar y detener la grabación
app_lock = e32.Ao_lock()
app_lock.wait()