import socket
import threading
import json 
import USER_INTERFACE.audioFrame.NOAA_DATA as NOAA_DATA
# Dirección IP y puerto en localhost
host = 'localhost'
port = 12345  # Reemplaza con el puerto que desees utilizar


class ClientSocket:
    def __init__(self, host, port, receive_callback):
        self.host = host
        self.port = port
        self.receive_callback = receive_callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.receive_thread = None

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            data = {
                "name": "MASTER",
                "type" : "ctr"
            }
            json_data = json.dumps(data)
            self.socket.send(json_data.encode('utf-8'))
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.start()
        except ConnectionRefusedError:
            print("No se pudo establecer la conexión. Asegúrate de que el servidor esté en ejecución.")

    def send(self, data):
        if self.connected:
            self.socket.send(data.encode('utf-8'))

    def receive_data(self):
        while self.connected:
            try:
                response = self.socket.recv(1024)
                if not response:
                    break
                response_data = response.decode('utf-8')
                if self.receive_callback:
                    self.receive_callback(response_data)
            except ConnectionResetError:
                break

    def disconnect(self):
        self.connected = False
        self.socket.close()
        if self.receive_thread:
            self.receive_thread.join()
 







import math
import time

def generar_onda(freq, duracion):
    tiempo_inicial = time.time()

    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial

        # Si ha pasado un segundo, emite el valor de la onda senosoidal
        if tiempo_transcurrido >= 1:
            # Calcula el valor de la onda senosoidal escalado y desplazado

            tiempo_inicial = time.time()

        # Si ha alcanzado la duración deseada, sale del bucle
        if tiempo_transcurrido >= duracion:
            break

# Frecuencia de la onda senosoidal (Hz)
if __name__ == "__main__":

    socketA=ClientSocket("192.168.100.17",12345,receive_callback=call)
    socketA.connect()
    listaPoint=NOAA_DATA.get_dataNOAA("32401")
    print(listaPoint[0])
    print(listaPoint[0][2])
    frecuencia = 1

# Duración total de la generación (segundos)
    duracion_total = 10000

# Llama a la función para generar la onda senosoidal
    tiempo_inicial = time.time()
    state=True
    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial

        # Si ha pasado un segundo, emite el valor de la onda senosoidal
        if tiempo_transcurrido >= 10:
            if state: # Calcula el valor de la onda senosoidal escalado y desplazado
                dataA = {
                    "ID":"TW1",
                    "CMD": "MOV",
                    "M1": 0,
                    "M2": 4000,
                    "MV": 0
                }

                dataB = {
                    "ID":"TW2",
                    "CMD": "MOV",
                    "M1": -4000,
                    "M2": 4000,
                    "MV": 0
                }

    # Combinar dataA y dataB en un JSON más grande
                combined_data = [dataA, dataB]
                json_data = json.dumps(combined_data)
                socketA.send(json_data)
                state=False

            else:
                dataA = {
                    "ID":"TW1",
                    "CMD": "MOV",
                    "M1": 0,
                    "M2": -4000,
                    "MV": 0
                }

                dataB = {
                    "ID":"TW2",
                    "CMD": "MOV",
                    "M1": 4000,
                    "M2": -4000,
                    "MV": 0
                }

    # Combinar dataA y dataB en un JSON más grande
                combined_data = [dataA, dataB]
                json_data = json.dumps(combined_data)
                socketA.send(json_data)
                state=True

            tiempo_inicial = time.time()                
        # Si ha alcanzado la duración deseada, sale del bucle
        if tiempo_transcurrido >= duracion_total:
            break


    
