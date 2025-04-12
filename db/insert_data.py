import asyncpg
from db.connection import get_db_pool

async def insert_data_from_dict(data):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        for date, table_data in data.items():
            for key, values in table_data.items():
                for value in values:
                    await conn.execute('''
                        INSERT INTO variacoes (ativo, tipo, referencia, valor)
                        VALUES ($1, $2, $3, $4)
                    ''', value["Ativo"], key, date, value["Valor"])
