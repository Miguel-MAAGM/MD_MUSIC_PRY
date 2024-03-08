import socket
import threading
import asyncio
import json

# Configura el servidor
HOST = 'localhost'  # Escucha en todas las interfaces
PORT = 12345      # Puerto para la comunicación

# Diccionario para mantener un registro de las conexiones de los ESP32
connections = {}
connections_data=[]
def is_json(data):
    try:
        json.loads(data)
        return True
    except json.decoder.JSONDecodeError:
        print("noJson")
        return False
    
def isNewclient(address):
    for client in connections_data:
        if  address == client["client"]:
            return True
    return False

def handle_client(client_socket, client_address):
    # Recibe datos del cliente
    FLAG =True
    try:
        while FLAG:

            data = client_socket.recv(1024)
    
            if not data:
                break
            if data == b'\r\n':
                break
            
            try:
                # Decodifica los datos JSON
                if not isNewclient(client_address):
                    if is_json(data.decode('utf-8')):
                        json_data = json.loads(data.decode('utf-8'))
                        client_data = {
                        "client": client_address,
                        "Type": json_data["type"],
                        "Name": json_data["name"],
                        "socket":client_socket
                        }
                        connections_data.append(client_data)
                    else:
                        print(data.decode('utf-8'))
                    #print(f"Recibido desde {client_address}: {json_data}")

                    # Procesa los datos según sea necesario
                    
                    # Envía una respuesta al cliente
                    response ={"type":"OK"} 
                    json_data = json.dumps(response)
                    client_socket.send(json_data.encode('utf-8'))
                else:
                    if is_json(data.decode('utf-8')):
                        if is_json(data.decode('utf-8')):
                            parsed_data = json.loads(data.decode('utf-8'))
                            for data in parsed_data:
                                ID  = data ["ID"]
                                CMD = data["CMD"]
                                M1 = data["M1"]
                                M2 = data["M2"]
                                MV = data["MV"]
                                indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] ==ID]
                                if indice==[]:
                                    print("no existe")
                                else:
                                    data = {
                                        "CMD": "MOV",
                                        "M1": M1,
                                        "M2": M2,
                                        "MV":MV
                                    }
                                    json_data = json.dumps(data)
                                    sendData(f"{json_data}", connections_data[indice[0]]["socket"])


                    else:
                        print(data.decode('utf-8'))
                    #print(f"Recibido desde {client_address}: {json_data}")

                    # Procesa los datos según sea necesario
                    
                    # Envía una respuesta al cliente
                    response ={"type":"OK"} 
                    json_data = json.dumps(response)
                    client_socket.send(json_data.encode('utf-8'))

            except json.decoder.JSONDecodeError as e:
                print(f"Error al analizar JSON: {e}")
    except ConnectionResetError:
        # Manejar la desconexión inesperada
        indice = [index for index, client_data in enumerate(connections_data) if client_data["client"] == client_address]
        del connections_data[indice[0]]

        print(f"Conexión con {client_address} cerrada inesperadamente: ")

 
        #print(client_data)
    # Cierra la conexión con el cliente
    #client_socket.close()
    #del connections[client_address]
def sendData(data,socket):
    print(len(connections))
    try:
        forSend = data+"\n"
        socket.send(forSend.encode('utf-8')) 
    except :
        # Manejar errores de conexión aquí, por ejemplo, si el cliente se desconecta
        print(f"Error al enviar datos al socket en {socket}")
    #for client in connections.values():

    #    json_data = json.dumps(data)
    #    client.send(json_data.encode('utf-8'))

def switch_case(option):
    rama=[]
    rama=option.split()
    print(rama)
    if rama[0] == "HOME":


        return "Opción 1 seleccionada"

    elif rama[0] == "MOV":
        indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] == rama[1]]
        print(indice)
        
        if indice==[]:
            print("no existe")
        else:
            data = {
                "CMD": "MOV",
                "M1": rama[2],
                "M2": rama[3],
                "MV": rama[4]
            }
            json_data = json.dumps(data)
            sendData(f"{json_data}", connections_data[indice[0]]["socket"])
        
        
        return "Opción 2 seleccionada"
    elif rama[0] == "GET":
        indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] == rama[1]]
        print(indice)
        
        if indice==[]:
            print("no existe")
        else:
            data = {
                "CMD": "GET"
            }
            json_data = json.dumps(data)
            sendData(f"{json_data}", connections_data[indice[0]]["socket"])

        return "Opción 3 seleccionada"
    elif rama[0] == "SET":
        sendData("SET INFO")
        return "Opción 3 seleccionada"
    elif rama[0]=="LIST":
        print(connections_data)
    else:
        return "Opción no válida"

def read_console_input():
    while True:
        # Envía el mensaje a todos los clientes conectados
        try:
            input_data = input("Ingrese un comando (HOME,LIST ,MOV, SET VEL, SET ACC): ").strip()
            print(input_data)
            if input_data == 0:
                break
            print(switch_case(input_data))
        except EOFError:
            # Se captura el EOFError y se maneja adecuadamente   
            print("Entrada de usuario finalizada.")
            


if __name__ == "__main__":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")
    console_input_thread = threading.Thread(target=read_console_input)
    console_input_thread.start()

    while True:
        client_socket, client_address = server.accept()
        
        #print(f"Conexión entrante desde {client_address}")
        
        connections[client_address] = client_socket
        
        # Inicia un hilo para manejar la conexión con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
        