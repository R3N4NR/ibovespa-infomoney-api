import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from service.flask_server import create_flask_app
from service.websocket_server import start_websocket_server
from service.server import scrape_loop, run_http_server
from db import handle_create_database


async def run_all():
    print("Iniciando todos os serviços...")
    await asyncio.gather(
        scrape_loop(),
        handle_create_database(),
        start_websocket_server(),  
        run_http_server()          
    )

if __name__ == "__main__":
    asyncio.run(run_all())
