import socket
import threading
import asyncio
import json

# Configura el servidor
HOST = 'LocalHost'  # Escucha en todas las interfaces
PORT = 12345      # Puerto para la comunicación

# Diccionario para mantener un registro de las conexiones de los ESP32
connections = {}
connections_data=[]
def is_json(data):
    try:
        json.loads(data)
        return True
    except json.decoder.JSONDecodeError:
        return False
    
def isNewclient(address):
    for client in connections_data:
        if  address == client["client"]:
            return True
    return False

def handle_client(client_socket, client_address):
    # Recibe datos del cliente
    FLAG =True
    print("\n NEW DEVICE CONECTED : ")
    try:
        while FLAG:

            data = client_socket.recv(1024)
    
            if not data:
                break
            if data == b'\r\n':
                break
            
            try:
                # Decodifica los datos JSON
                if is_json(data.decode('utf-8')):
                    json_data = json.loads(data.decode('utf-8'))
                    name=json_data["nombre"]
                    print(f"{name}\n")
                    client_data = {
                    "client": client_address,
                    "Type": json_data["type"],
                    "Name": json_data["nombre"]
                    }
                    connections_data.append(client_data)
                else:
                    print(data.decode('utf-8'))
                #print(f"Recibido desde {client_address}: {json_data}")

                # Procesa los datos según sea necesario
                
                # Envía una respuesta al cliente
                response = "OK"
                client_socket.send(response.encode('utf-8'))
            
            except json.decoder.JSONDecodeError as e:
                print(f"Error al analizar JSON: {e}")
    except ConnectionResetError:
        # Manejar la desconexión inesperada
        print(f"Conexión con {client_address} cerrada inesperadamente: ")
    finally:
        client_socket.close()
 
        #print(client_data)
    # Cierra la conexión con el cliente
    #client_socket.close()
    #del connections[client_address]
def sendData(data):
    print(len(connections))
    for client in connections.values():

        json_data = json.dumps(data)
        client.send(json_data.encode('utf-8'))

def switch_case(option):
    if option == "HOME":
        
        sendData("HOME")

        return "Opción 1 seleccionada"

    elif option == "MOV":
        sendData("MOV")
        return "Opción 2 seleccionada"
    elif option == "SET VEL":
        sendData("SET VEL")
        return "Opción 3 seleccionada"
    elif option == "SET ACC":
        sendData("SET ACC")
        return "Opción 3 seleccionada"

    else:
        return "Opción no válida"

def read_console_input():
    while True:
        # Envía el mensaje a todos los clientes conectados
        try:
            input_data = input("Ingrese un comando (HOME, MOV, SET VEL, SET ACC): ").strip()
            print(input_data)
            if input_data == 0:
                break
            print(switch_case(input_data))
        except EOFError:
            # Se captura el EOFError y se maneja adecuadamente   
            print("Entrada de usuario finalizada.")
            
def main():

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
        

if __name__ == "__main__":

    main()
    