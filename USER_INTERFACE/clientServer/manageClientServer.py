import socket
import threading
import json 
import time
PORT = 12345      # Puerto para la comunicación

class manageClientServer:
    def __init__(self, host, port,  clb_List=None,
                                    clb_GetInf=None,
                                    clb_pipeline=None):
        self.host = host
        self.port = port
        self.clb_List = clb_List
        self.clb_GetInf = clb_GetInf
        self.clb_Pipeline = clb_pipeline
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.receive_thread = None
        self.type=[]

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
                print(response)
                if(self.is_json(response.decode('utf-8'))):
                    response_data = json.loads(response.decode('utf-8'))
                    print("Paquete recibido como JSON:", response_data)
                    self.switch_case(self.type.pop(0),response_data)
            except ConnectionAbortedError:
                print("La conexión fue anulada por el software en el equipo host.")
                break
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                break

    def disconnect(self):
        self.connected = False
        self.socket.close()
        if self.receive_thread:
            self.receive_thread.join()
 


    def is_json(self,data):
        try:
            json.loads(data)
            return True
        except ValueError:
            return False
    
    def getInfoDev(self,messege):
        data= {
            "CMD":"GET",
            "ID":messege
        }
        json_data = json.dumps(data)
        self.send(json_data)
        self.type.append("GET_Data")
        return 
    def setInfoDev(self,messege):
        json_data = json.dumps(messege)
        self.send(json_data)
        return
    def getListDev(self):
        data= {
            "CMD":"LIST"
        }
        json_data = json.dumps(data)
        self.send(json_data)
        self.type.append("LIST")
         
    def sendPoint(self,messege):
        
        return


    def case_default(self):
        print("Type no Valid")
        return True 
    def response_List(self,messege):
        if self.clb_List:
            self.clb_List(messege)
    def response_Pipeline(self,messege):
        if self.clb_Pipeline:
            self.clb_Pipeline(messege)
    def response_GetData(self,messege):
        if self.clb_GetInf:
            self.clb_GetInf(messege)
         
   
    def switch_case(self,Type, messege):
        if (Type=="LIST"):
           self.response_List(messege)
        if (Type=="GET_Data"):
           self.response_GetData(messege)
def calb(data):
    print(data)
def calb_m(data):
    print(data)
def calb_pi(data):
    print(data)
if __name__ == "__main__":


    server =manageClientServer(socket.gethostbyname(socket.gethostname()),PORT,clb_List=calb,clb_GetInf=calb_m,clb_pipeline=calb_pi)

    server.connect()
    time.sleep(5)

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
    dataC = {
            "ID":"TW3",
            "CMD": "MOV",
            "M1": -4000,
            "M2": 4000,
            "MV": 0
        }
    dataD = {
            "ID":"TW4",
            "CMD": "MOV",
            "M1": -4000,
            "M2": 4000,
            "MV": 0
        }
    data_master={
        "CMD":"MOV",
        "TW1":dataA,
        "TW2":dataB,
        "TW3":dataC,
        "TW4":dataD
    }
    json_data = json.dumps(data_master)
    print(json_data)
    server.send(json_data)

    #server.getListDev()