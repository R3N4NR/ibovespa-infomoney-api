import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from service.flask_server import create_flask_app
from service.websocket_server import start_websocket_server
from db import handle_create_database
async def run_http_server():
    app = create_flask_app()
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    # Executa o servidor Flask com Hypercorn (assíncrono)
    await serve(app, config)

async def run_all():
    print("Iniciando todos os serviços...")
    await asyncio.gather(
        handle_create_database(),
        start_websocket_server(),  # Inicia o WebSocket
        run_http_server()          # Inicia o Flask
    )

if __name__ == "__main__":
    asyncio.run(run_all())
