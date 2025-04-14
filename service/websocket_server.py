import asyncio
import websockets
import json

connected_clients = set()
command_callback = None

def set_callback_command(callback):
    global command_callback
    command_callback = callback

async def send_to_all_clients(data):
    if connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def handler(websocket, path):
    connected_clients.add(websocket)
    print("Cliente conectado.")
    try:
        await websocket.send(json.dumps({"message": "Conectado com sucesso"}))
        while True:
            try:
                message = await websocket.recv()
                print(f"Comando recebido do cliente: {message}")
                if command_callback:
                    await command_callback(message)
            except websockets.ConnectionClosed:
                print(f"Conexão fechada com o cliente {websocket.remote_address}")
                break
            except Exception as e:
                print(f"Erro inesperado com cliente {websocket.remote_address}: {e}")
                break
    finally:
        connected_clients.remove(websocket)
        print(f"Cliente {websocket.remote_address} desconectado.")

async def start_websocket_server():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Servidor WebSocket iniciado na porta 8765")
    await server.wait_closed()

# Inicia o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(start_websocket_server())
