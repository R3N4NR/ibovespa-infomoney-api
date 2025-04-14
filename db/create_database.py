import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def handle_create_database():
    db_name = os.getenv("DB_NAME")
    try:
        # Conecta ao banco postgres padrão
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="postgres"
        )

        # Verifica se o banco já existe
        result = await conn.fetch("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not result:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Banco '{db_name}' criado.")
        else:
            print(f"Banco '{db_name}' já existe.")
        await conn.close()

        # Conecta ao banco alvo
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=db_name
        )

        # Criação da tabela se não existir
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id UUID PRIMARY KEY,
                ativo TEXT NOT NULL,
                ultimo TEXT,
                variacao TEXT,
                val_min TEXT,
                val_max TEXT,
                date TEXT NOT NULL
            );
        """)

        # Garante que a constraint de unicidade (ativo, date) exista
        await conn.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'unique_ativo_date'
                ) THEN
                    ALTER TABLE stocks ADD CONSTRAINT unique_ativo_date UNIQUE (ativo, date);
                END IF;
            END
            $$;
        """)

        print("Tabela 'stocks' verificada/criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco ou tabela: {str(e)}")
    finally:
        await conn.close()
