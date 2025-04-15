import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

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
        await conn.close()

        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=db_name
        )


        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id UUID PRIMARY KEY,
                ativo TEXT NOT NULL,
                ultimo TEXT,
                variacao TEXT,
                val_min TEXT,
                val_max TEXT,
                date TEXT NOT NULL,
                UNIQUE (ativo, date)
            );
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS ibovespa_summary (
                id UUID PRIMARY KEY,
                pontos TEXT,
                variacao_dia TEXT,
                min_dia TEXT,
                max_dia TEXT,
                date TEXT NOT NULL UNIQUE
            );
        """)

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
        await conn.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'unique_date'
                ) THEN
                    ALTER TABLE ibovespa_summary ADD CONSTRAINT unique_date UNIQUE (date);
                END IF;
            END
            $$;
        """)

        print("Tabela 'stocks' e 'ibovespa_overview' verificadas/criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco ou tabela: {str(e)}")
    finally:
        await conn.close()
