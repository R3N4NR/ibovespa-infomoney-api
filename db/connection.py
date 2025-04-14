import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_db_pool():
    try:
        return await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        min_size=1,
        max_size=10
    )
    except Exception as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")
