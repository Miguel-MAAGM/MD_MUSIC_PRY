import socket
import threading
import json 
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
                if not response:
                    break
                response_data = json.loads(response.decode('utf-8'))
                print("Paquete recibido como JSON:", response_data)
                if 'type' in response_data:
                    tipo = response_data['type']
                    if tipo == "OK":
                        print("Conexcion Creada :D")
                    else:
                        otros_datos = response_data['datos']
                        self.switch_case(tipo,otros_datos)
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
 
    def get_listDevice(self):
        #obtencion de la lista de device
        return True


    def getInfoDev(self,messege):

        return 
    def setInfoDev(self,messege):

        return
    def getListDev(self,messege):

        return 
    def sendPoint(self,messege):
        
        return


    def case_default(self):
        print("Type no Valid")
        return True 
    def response_List(self,messege):
        if self.clb_List:
            self.clb_List(messege)
        return True
    def response_Pipeline(self,messege):
        if self.clb_Pipeline:
            self.clb_Pipeline(messege)
        return True
    def response_GetData(self,messege):
        if self.clb_GetInf:
            self.clb_GetInf(messege)
        return True
         
   
    def switch_case(self,Type, messege):
        switch_dict = {
            "LIST": self.response_List(messege),
            "PIPELINE":self.response_Pipeline(messege),
            "GETDATA":self.response_GetData(messege),
            
        }
        return switch_dict.get(Type, self.case_default)()


if __name__ == "__main__":


    manageClientServer(socket.gethostbyaddr,PORT,)