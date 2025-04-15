from db import get_db_pool
import uuid
async def insert_data_from_table(data):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        for date_key, table_data in data.items():
            for key, values in table_data.items():
                for value in values:
                    ativo = value.get("Ativo")
                    ultimo = value.get("Último (R$)")
                    variacao = value.get("Var. Dia (%)")
                    val_min = value.get("Val. Min (R$)")
                    val_max = value.get("Val. Máx (R$)")
                    date = value.get("Data")
                    id = value.get("ID")
                    print(ativo, ultimo, variacao, val_min, val_max, date, uuid )
        

                    await conn.execute('''
                        INSERT INTO stocks (id, ativo, ultimo, variacao, val_min, val_max, date)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        ON CONFLICT (ativo, date) DO UPDATE
                        SET
                            ultimo = EXCLUDED.ultimo,
                            variacao = EXCLUDED.variacao,
                            val_min = EXCLUDED.val_min,
                            val_max = EXCLUDED.val_max
                    ''', id, ativo, ultimo, variacao, val_min, val_max, date)

async def insert_ibovespa_summary(data):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        id = data.get("ID")
        pontos = data.get("Pontos")
        variacao_dia = data.get("Variação (dia)")
        min_dia = data.get("Mín (Dia)")
        max_dia = data.get("Máx (Dia)")
        date = data.get("Date")

        await conn.execute("""
            INSERT INTO ibovespa_summary (id, pontos, variacao_dia, min_dia, max_dia, date)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (date) DO UPDATE
            SET 
                pontos = EXCLUDED.pontos,
                variacao_dia = EXCLUDED.variacao_dia,
                min_dia = EXCLUDED.min_dia,
                max_dia = EXCLUDED.max_dia
        """, id, pontos, variacao_dia, min_dia, max_dia, date)
