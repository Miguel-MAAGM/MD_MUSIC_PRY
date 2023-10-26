import NOAA_DATA
import socket
import json 
import matplotlib.pyplot as plt
import signal
import sys
import atexit
#data=NOAA_DATA.get_dataNOAA("34420")
#altura=[]
#
#for items in data:
#    altura.append(items[2])
#
#valor_medio = sum(altura) / len(altura)
#
#datos_restantes = [x - valor_medio for x in altura]
#valor_min = min(altura)
#valor_max = max(altura)
#
## Aplicar la normalización min-max
#datos_normalizados = [(x - valor_min) / (valor_max - valor_min) for x in altura]
#
#plt.plot(range(len(datos_restantes)), datos_restantes)
#
#plt.xlabel("Índice de datos")
#plt.ylabel("Datos con valor medio restado")
#
#plt.show()
#print(f"media es:  {valor_medio}")

# Dirección IP y puerto en localhost
host = 'localhost'
port = 12345  # Reemplaza con el puerto que desees utilizar

# Datos en formato JSON
data = {
    "nombre": "MASTER"
}
json_data = json.dumps(data)  # Convierte el diccionario en una cadena JSON

# Crear un socket
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

def signal_handler(sig, frame):
    print("Se ha recibido la señal SIGINT (Ctrl+C). Realizando tareas de cierre...")
    
    s.close

    sys.exit(0)
def exit_handler():

    print("El programa se está cerrando.")
    s.close

atexit.register(exit_handler)

signal.signal(signal.SIGINT, signal_handler)
while True:
    input_Data=input("Send Something")
    s.send(input_Data.encode('utf-8'))


