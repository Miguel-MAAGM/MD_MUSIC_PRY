import socket
import threading
import asyncio
import json

PORT = 12345      # Puerto para la comunicación

connections = {}
connections_data=[]
def buscar_y_reemplazar_por_nombre( nombre, nuevo_elemento):
    for i, elemento in enumerate(connections_data):
        if elemento.get('Name') == nombre:
            del connections_data[i]  # Elimina el elemento de la lista
            connections_data.append(nuevo_elemento)  # Agrega el nuevo elemento al final de la lista
            return True  # Retorna True si se encontró y reemplazó el elemento
    
    return False

def is_json(data):
    try:
        json.loads(data)
        return True
    except json.decoder.JSONDecodeError:
        return False
def detectar_ip_repetida(lista, ip_nuevo):
    ips = [entry['client'][0] for entry in lista]
    if ip_nuevo in ips:
        return True  # La dirección IP ya existe en la lista
    else:
        return False  #
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

            try:
                # Decodifica los datos JSON
                if not isNewclient(client_address):
                    print("no existe")
                    if is_json(data.decode('utf-8')):
                        json_data = json.loads(data.decode('utf-8'))
                        client_data = {
                        "client": client_address,
                        "Type": json_data["type"],
                        "Name": json_data["name"],
                        "socket":client_socket
                        }
                        if not (buscar_y_reemplazar_por_nombre(json_data["name"],client_data)):
                            print("Se agrega Nuevo")
                            connections_data.append(client_data)  # Agrega el nuevo elemento al final de la lista
                        else:
                            print("Find and replace")
                        
                    else:
                        print(data.decode('utf-8'))
                    json_data = "OK\n"
                    client_socket.send(json_data.encode('utf-8'))
                else:
                    if is_json(data.decode('utf-8')):
                        parsed_data = json.loads(data.decode('utf-8'))
                        if "CMD" in parsed_data:
                                if parsed_data["CMD"]=="RES":
                                    indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] =="MASTER"]
                                    print("Try Sending")
                                    if indice==[]:
                                        print("NO existe MASTER")
                                    else:   
                                        messeg={
                                           "M1": parsed_data["M1"],
                                           "M2": parsed_data["M2"],
                                           "MVI": parsed_data["MVI"]
                                        }
                                        json_data = json.dumps(messeg)
                                        sendData(f"{json_data}", connections_data[indice[0]]["socket"])
                                    
                                if parsed_data["CMD"]=="SET":
                                    indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] ==parsed_data["ID"]]
                                    motorData=parsed_data["MX"]
                                    if indice==[]:
                                        print("NO existe MASTER")
                                    else: 
                                        messeg={
                                            "CMD":"SET",
                                            "M1": motorData["M1"],
                                            "M2": motorData["M2"],
                                            "MVI": motorData["MVI"]
                                        }
                                        json_data = json.dumps(messeg)
                                        sendData(f"{json_data}", connections_data[indice[0]]["socket"])
                                    
                                if parsed_data["CMD"]=="MOV":
                                    print("MOV")
                                    start_iterating = False
                                    clave_inicial="TW1"
                                    for data in parsed_data:
                                        if data == clave_inicial:
                                            start_iterating = True

                                        if start_iterating:
                                            print(data)
                                            element=parsed_data[data]
                                            indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] ==element["ID"]]
                                            if indice==[]:
                                               print("no existe")
                                            else:
                                                cmd = {
                                                   "CMD": "MOV",
                                                   "M1": element["M1"],
                                                   "M2": element["M2"],
                                                   "MV":element["MV"]
                                                }
                                                json_data = json.dumps(cmd)
                                                sendData(f"{json_data}", connections_data[indice[0]]["socket"])

                                if parsed_data["CMD"]=="STOP":
                                    
                                    
                                    print(parsed_data)
                                if parsed_data["CMD"]=="HOME":
                                    indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] ==parsed_data["ID"]]
                                    print(indice)
                                    if indice==[]:
                                        print("no existe")
                                    else:
                                        data = {
                                            "CMD": "HOME"
                                        }

                                    print(parsed_data)                                   
                                if parsed_data["CMD"]=="GET":
                                    indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] == parsed_data["ID"]]
                                    print(indice)
                                    if indice==[]:
                                        print("no existe")
                                    else:
                                        data = {
                                            "CMD": "GET"
                                        }
                                    json_data = json.dumps(data)
                                    sendData(f"{json_data}", connections_data[indice[0]]["socket"])
                                    print(parsed_data)
                                if parsed_data["CMD"]=="LIST":
                                    indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] =="MASTER"]
                                    filtered_names = [item['Name'] for item in connections_data if item['Name'] != 'MASTER']
                                    json_data = json.dumps(filtered_names)
                                    sendData(f"{json_data}", connections_data[indice[0]]["socket"])
                                    print("LIST")
                                if parsed_data["CMD"]=="PIPE":
                                    msg=parsed_data["MSG"]
                                    print(msg)
                                    switch_case(msg)


                    # Procesa los datos según sea necesario
                    
                    # Envía una respuesta al cliente
                    print("response")
                    json_data = "OK\n"
                    client_socket.send(json_data.encode('utf-8'))

            except json.decoder.JSONDecodeError as e:
                print(f"Error al analizar JSON: {e}")
    except ConnectionResetError:
        # Manejar la desconexión inesperada
        indice = [index for index, client_data in enumerate(connections_data) if client_data["client"] == client_address]
        del connections_data[indice[0]]

        print(f"Conexión con {client_address} cerrada inesperadamente: ")

 
def sendData(data,socket):
    try:
        forSend = data+"\n"
        socket.send(forSend.encode('utf-8')) 
    except :
        print(f"Error al enviar datos al socket en {socket}")


def switch_case(option):
    rama=[]
    rama=option.split()
    if rama[0] == "HOME":


        return "Opción 1 seleccionada"

    elif rama[0] == "MOV":
        indice = [index for index, client_data in enumerate(connections_data) if client_data["Name"] == rama[1]]
        
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
        try:
            input_data = input("Ingrese un comando (HOME,LIST ,MOV, SET VEL, SET ACC): ").strip()
            if input_data == 0:
                break
            print(switch_case(input_data))
        except EOFError:
            print("Entrada de usuario finalizada.")
            server.close()

            break
            
            


if __name__ == "__main__":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host =socket.gethostbyname(socket.gethostname())
    
    server.bind((host, PORT))
    server.listen(10)
    print(f"Servidor escuchando en {host}:{PORT}")
    console_input_thread = threading.Thread(target=read_console_input)
    console_input_thread.start()
    try:
        while True:
            client_socket, client_address = server.accept()

            #print(f"Conexión entrante desde {client_address}")


            # Inicia un hilo para manejar la conexión con el cliente
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        server.close()
        print("APP close")
