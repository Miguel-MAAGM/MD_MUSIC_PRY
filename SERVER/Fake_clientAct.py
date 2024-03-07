import socket
import json 
host = 'localhost'
port = 12345  # Reemplaza con el puerto que desees utilizar


inputdata= input("NAME FAKE:")
data = {
    "name": inputdata,
    "type" : "act"
}
json_data = json.dumps(data)  # Convierte el diccionario en una cadena JSON
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
        # Conectar al servidor en localhost y puerto específico
        s.connect((host, port))

        # Enviar los datos al servidor
        s.send(json_data.encode('utf-8'))

        # Esperar una respuesta (opcional)
        response = s.recv(1024)
        print("Respuesta del servidor:", response.decode('utf-8'))
except ConnectionRefusedError:
        print("No se pudo establecer la conexión. Asegúrate de que el servidor esté en ejecución.")
while True:
    send_DATA=input("DATA: ")
    s.send(send_DATA.encode('utf-8'))