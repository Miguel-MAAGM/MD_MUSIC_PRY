
import socket
import json
import threading
def handle_client(client_socket, client_address):
    # Recibe datos del cliente
    
    try:
        while True:

            data = client_socket.recv(1024)
            

    except ConnectionResetError:
        # Manejar la desconexión inesperada
        print(f"Conexión con {client_address} cerrada inesperadamente: ")



def read_console_input():
    while True:
        try:
            input_data = input("Ingrese un comando (HOME,LIST ,MOV, SET VEL,STOP ,SET ACC): ").strip()
            print(input_data)
            if input_data == 0:
                break
            if input_data== "GET":
                json_data = json.dumps({"CMD": "GET"})+"\n"
                client_socket.sendall(json_data.encode('utf-8'))
            
            
            #print(switch_case(input_data))
        except EOFError:
            print("Entrada de usuario finalizada.")
            server.close()

            break
    
if __name__ == "__main__":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host =socket.gethostbyname(socket.gethostname())
    
    server.bind((host, 12345))
    server.listen(10)
    print(f"Servidor escuchando en {host}:{12345}")
    console_input_thread = threading.Thread(target=read_console_input)
    console_input_thread.start()
    try:
        while True:
            client_socket, client_address = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        server.close()
        print("APP close")


#if __name__ == "__main__":
#    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    host =socket.gethostbyname(socket.gethostname())
#   
#    server_socket.bind((host, 12345))
#
#    server_socket.listen(5)
#
#    print('Servidor escuchando en', 12345)
#    while True:
#                client_socket, client_address = server_socket.accept()
#
#                #print(f"Conexión entrante desde {client_address}")
#
#
#                # Inicia un hilo para manejar la conexión con el cliente
#                client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
#                client_handler.start()
#
#
    #            
    #while True:
    #    client_socket, address = server_socket.accept()
    #    print('Conexión entrante desde:', address)
    #
    #    # Leer datos JSON del cliente
    #    data = client_socket.recv(1024).decode('utf-8')
    #    print('Datos JSON recibidos del cliente:', data)
    #
    #    # Enviar datos JSON al cliente
    #    json_data = json.dumps({"message": "Hola desde Python", "value": 456})
    #    client_socket.sendall(json_data.encode('utf-8'))
    #
    #    client_socket.close()