import socket
import threading
import json 
import NOAA_DATA
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
 
def call(data):
    print(data)
if __name__ == "__main__":

    socketA=ClientSocket("192.168.100.17",12345,receive_callback=call)
    socketA.connect()
    listaPoint=NOAA_DATA.get_dataNOAA("32401")
    print(listaPoint[0])
    print(listaPoint[0][2])
    while True:
        data = input("text somthing :")
        buf=[]
        
        buf = data.split()
        
        dataA = {
            "ID":"TW1",
            "CMD": "MOV",
            "M1": 500,
            "M2": 500,
            "MV": 500
        }

        dataB = {
            "ID":"TW2",
            "CMD": "MOV",
            "M1": buf[0],
            "M2": buf[1],
            "MV": buf[2]
        }
        dataC = {
            "ID":"TW3",
            "CMD": "MOV",
            "M1": buf[0],
            "M2": buf[1],
            "MV": buf[2]
        }

    # Combinar dataA y dataB en un JSON más grande
        combined_data = [dataA, dataB]
        json_data = json.dumps(combined_data)
        socketA.send(json_data)
    