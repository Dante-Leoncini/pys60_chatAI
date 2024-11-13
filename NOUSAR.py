# -*- coding: utf-8 -*-
import appuifw
import e32
import graphics

# Configuración inicial de la interfaz
appuifw.app.title = u"Chat"  # Título en la barra superior
appuifw.app.screen = 'normal'  # Modo de pantalla completa

canvas = appuifw.Canvas()
appuifw.app.body = canvas

# Texto a mostrar
texto = u"¡Hola, mundo!"

# Fuente de texto
fuente = "dense"

# Dibujar el texto en rojo
def dibujar_texto():
    canvas.clear(0xEEEEEE)  # Limpiar el canvas
    x = 0
    y = 40
    canvas.text((x, y), texto, fill=0xFF0000, font=fuente)  # Dibujar el texto

dibujar_texto()

# Función para manejar las teclas
def handle_key(event):
    global texto
    if event['type'] == appuifw.EEventKey:
        key_code = event['keycode']

        if key_code == 63557:  # Tecla de "Enter" o "Enviar" en algunos dispositivos Symbian
            texto = u"apretaste enter"
            pass  # No hacer nada, ya que no queremos enviar nada por ahora

        elif key_code == 8:  # Retroceso
            texto = texto[:-1]  # Eliminar el último carácter

        else:
            texto += unichr(key_code)  # Agregar el carácter al texto

        dibujar_texto()  # Actualizar el texto en el canvas

# Asignar la función de manejo de teclas al canvas
canvas.bind(appuifw.EEventKey, handle_key)

# Menú simple
appuifw.app.menu = [(u"Opción 1", lambda: None), (u"Opción 2", lambda: None)]

# Mantener la aplicación corriendo hasta que se cierre
def salir():
    app_lock.signal()

appuifw.app.exit_key_handler = salir
app_lock = e32.Ao_lock()
app_lock.wait()