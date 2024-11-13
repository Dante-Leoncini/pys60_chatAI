# -*- coding: utf-8 -*-
import httplib
import appuifw
import e32
import graphics
import os
import base64

canvas = appuifw.Canvas()
appuifw.app.body = canvas
canvas.clear(0xEEEEEE)  # Limpiar el canvas

proxy_url = '192.168.0.59:5000'  # Reemplaza con la IP y puerto de tu proxy
path = '/imageproxy'

headers = {
    'Content-Type': 'application/json'
}

# Pedir al usuario que ingrese texto
user_input = appuifw.query(u"¿Que imagen quieres generar?:", "text")

json_data = (
    '{"inputs": "'+user_input+'"}'
)

wait_dialog = None
timer = e32.Ao_timer()

def show_wait_dialog():
    global wait_dialog
    wait_dialog = appuifw.note(u"Cargando, por favor espera...", "info")

def hide_wait_dialog():
    global wait_dialog
    if wait_dialog:
        wait_dialog = None

def fetch_and_display_image():
    try:
        # Mostrar el diálogo de espera
        show_wait_dialog()

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
        
        # Cargar y dibujar la imagen en el Canvas
        img = graphics.Image.open(image_path)
        # Redimensionar la imagen a 320x320px
        img_resized = img.resize((240, 240))
        # Dibujar la imagen redimensionada en el Canvas
        canvas.blit(img_resized, target=(0, 0))

    except Exception, e:
        print("Error al conectar con la API o procesar la imagen:", e)
    finally:
        # Ocultar el diálogo de espera después de recibir la respuesta o si hay error
        timer.after(0, hide_wait_dialog)

# Ejecutar la función para cargar y mostrar la imagen
fetch_and_display_image()

# Menú simple
appuifw.app.menu = [(u"Opción 1", lambda: None), (u"Opción 2", lambda: None)]

# Mantener la aplicación corriendo hasta que se cierre
def salir():
    app_lock.signal()

appuifw.app.exit_key_handler = salir
app_lock = e32.Ao_lock()
app_lock.wait()