import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from service.flask_server import create_flask_app
from service.websocket_server import start_websocket_server
import aiohttp

async def run_http_server():
    app = create_flask_app()
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    await serve(app, config)

async def scrape_loop():
    await asyncio.sleep(5)  # Pequeno delay após iniciar
    while True:
        try:
            
            print("🔄 Disparando scrape automático...")
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:5000/scrape") as resp:
                    text = await resp.text()
                    print(f"📦 Resposta do /scrape: {resp.status} - {text}")
        except Exception as e:
            print(f"❌ Erro ao chamar /scrape: {e}")
        await asyncio.sleep(900)  # Espera 15 minutos (900 segundos)

async def run_all():
    print("🚀 Iniciando todos os serviços...")
    await asyncio.gather(
       
        start_websocket_server(),  # WebSocket
        run_http_server(),         # Flask com Hypercorn
        scrape_loop()              # Scrape automático
    )

if __name__ == "__main__":
    asyncio.run(run_all())
