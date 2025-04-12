import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

#Verifica se o banco existe se não exite cria um novo
async def handle_create_database():
    db_name = os.getenv("DB_NAME")
    try:
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="postgres"
        )
    
        result = await conn.fetch("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not result:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Banco '{db_name}' criado.")
        else:
            print(f"Banco '{db_name}' já existe.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {str(e)}")
    finally:
        await conn.close()
