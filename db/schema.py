from db.connection import get_db_pool

async def create_table():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Habilita extensão de UUID se ainda não existir
        await conn.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                ativo TEXT,
                ultimo NUMERIC,
                variacao NUMERIC,
                val_min NUMERIC,
                val_max NUMERIC,
                data TEXT,
                UNIQUE (ativo)
            )
        """)
    await pool.close()
    print("Tabela 'stocks' verificada/criada.")
