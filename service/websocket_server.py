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
                break
    finally:
        connected_clients.remove(websocket)
        print("Cliente desconectado.")

async def start_websocket_server():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Servidor WebSocket iniciado na porta 8765")
    await server.wait_closed()
