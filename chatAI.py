# -*- coding: utf-8 -*-
import httplib
import appuifw
import e32

proxy_url = '192.168.0.59:5000'  # Reemplaza con la IP y puerto de tu proxy
path = '/chatproxy'

headers = {
    'Content-Type': 'application/json'
}

# Pedir al usuario que ingrese texto
user_input = appuifw.query(u"Ingrese su mensaje:", "text")

json_data = (
    '[{'
    '"role": "user",'
    '"content": "'+user_input+'"'
    '}]'
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
    
def clear_screen():
    """Función para limpiar la pantalla simulando un desplazamiento."""
    print("\n" * 50)  # Imprime 50 líneas en blanco para limpiar la pantalla

try:
    # Mostrar el diálogo de espera
    show_wait_dialog()

    conn = httplib.HTTPConnection(proxy_url)
    conn.request("POST", path, body=json_data, headers=headers)

    response = conn.getresponse()
    response_data = response.read()

     # Asegúrate de que los datos estén correctamente decodificados a UTF-8
    response_data = response_data.decode('utf-8')
        
    # Limpiar la pantalla antes de mostrar el resultado
    clear_screen()

    # Encuentra la posición donde comienza el valor de "response"
    start_index = response_data.find('"response":"') + len('"response":"')
    # Encuentra la posición donde termina el valor de "response"
    end_index = response_data.find('"', start_index)

    # Extrae el valor
    response_value = response_data[start_index:end_index]

    # Imprime el valor
    #appuifw.note(u(response_value))
    print(response_value)    
    wait_dialog = appuifw.note(response_value)

    conn.close()
except Exception, e:
    print("Error al conectar con la API:", e)
#finally:
    # Ocultar el diálogo de espera después de recibir la respuesta o si hay error
    #timer.after(0, hide_wait_dialog)
    #wait_dialog = appuifw.note(u"aaaaaa")