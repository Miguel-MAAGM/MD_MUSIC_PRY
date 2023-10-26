import asyncio
import websockets
import json

# Diccionario para mantener un registro de las conexiones de los ESP32
connections = {}
client_names = {}

async def handle_client(websocket, path):
    try:
        # Pide un nombre o identificador al cliente
        await websocket.send("*")
        name = await websocket.recv()

        # Almacena la conexión en el diccionario
        connections[websocket.remote_address] = websocket
        # Almacena el nombre en el diccionario de nombres
        client_names[websocket.remote_address] = name

        print(f"Cliente {websocket.remote_address} se identificó como {name}")

        while True:
            try:
                # Recibe datos del cliente
                data = await websocket.recv()

                # Decodifica los datos JSON
                json_data = json.loads(data)
                print(f"Recibido desde {websocket.remote_address}: {json_data}")

                # Procesa los datos según sea necesario

                # Envía una respuesta al cliente
                response = {"mensaje": "Respuesta desde el servidor"}
                await websocket.send(json.dumps(response))
            except websockets.ConnectionClosed:
                print(f"Conexión cerrada por el cliente {websocket.remote_address}")
                break

    except websockets.ConnectionClosed:
        pass

async def main():
    server = await websockets.serve(handle_client, "LocalHost", 12345)

    print("Servidor WebSocket iniciado")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())