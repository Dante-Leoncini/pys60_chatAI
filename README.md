# pys60_chatAI
Un chat básico que usa Llama-3.2-1B-Instruct y Python (pys60) para Symbian s60v3.

1) se necesita tener instalado python en tu nokia s60v3/s60v5/symbian belle! si es pys60 2.0.0 mejor.

![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/Screenshot0103.bmp)

3) Edita el archivo "proxyPC.py" y modifica "client = InferenceClient(api_key="hf_xxxxxxxx")" y pone tu api_key. la cual la conseguis en https://huggingface.co/
4) necesitas iniciar el proxy con python3 en una pc. ejemplo: "python3 proxyPC.py"
   
![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/PROXY.jpg)

nota: el proxy es debido a que symbian no tiene soporte para conexiones seguras TLS 1.2. esto capaz se pueda arreglar mas adelante con proyectos como https://nnp.nnchan.ru/tls/ pero por ahora no tiene soporte para python

5) abre pys60 y conectate a la red wifi donde esta tu PC con el proxy.
6) edita "chatAI.py" y cambia "proxy_url = '192.168.0.59:5000'" por la ip de tu PC.
7) en pys60 abri "Run Script". el script editado "proxyPC.py" tiene que estar en el disco C o E del telefono. en la carpeta "python". seleccionalo

![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/Screenshot0104.bmp)

8) escribi tu mensaje
    
![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/Screenshot0108.bmp)

9) espera...
    
![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/Screenshot0106.bmp)

10) var a ver la respuesta si todo salio bien
    
![](https://raw.githubusercontent.com/Dante-Leoncini/pys60_chatAI/refs/heads/main/capturas/Screenshot0109.bmp)
