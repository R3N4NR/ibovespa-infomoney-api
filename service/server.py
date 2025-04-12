import asyncio
from flask_server import create_flask_app
from websocket_server import start_websocket_server, set_callback_command
from main import main_loop, run_once
from hypercorn.asyncio import serve
from hypercorn.config import Config

async def handle_command(message):
    if message.lower() == "recarregar":
        print("Comando 'recarregar' recebido! Executando scraping manual...")
        await run_once()
    else:
        print(f"Comando desconhecido: {message}")

async def run_http_server():
    app = create_flask_app()
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    await serve(app, config)

async def run_all():
    print("Iniciando todos os serviços...")
    set_callback_command(handle_command)
    await asyncio.gather(
        main_loop(),
        start_websocket_server(),
        run_http_server()
    )

if __name__ == "__main__":
    asyncio.run(run_all())
