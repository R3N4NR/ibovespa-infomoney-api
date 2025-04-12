import asyncio
from service.flask_server import create_flask_app


async def run_http_server():
    app = create_flask_app()
    await app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    asyncio.run(run_http_server())