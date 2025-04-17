from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from scraper.html_scraper import scrape_html
from scraper.table_data_parser import extract_table_data, summary_info
from db import insert_data_from_table, insert_ibovespa_summary
from db import get_db_pool
from service.websocket_server import send_to_all_clients

def create_flask_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/scrape', methods=['GET'])
    async def scrape_route():
        html = await scrape_html()
        table_data = extract_table_data(html)
        summary_data = summary_info(html) 
        await insert_ibovespa_summary(summary_data)
        await insert_data_from_table(table_data)

        payload = {
            "summary": summary_data,
            "tables": table_data
        }

        await send_to_all_clients(payload)

        return jsonify({"status": "ok", "message": "Dados coletados, inseridos e enviados"}), 200

    @app.route('/stocks', methods=['GET'])
    async def get__stocks_name():
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT DISTINCT ativo FROM stocks;")
        await pool.close()

        ativos = [dict(row) for row in rows]
        return jsonify(ativos), 200


    @app.route('/stocks/<string:date>', methods=['GET'])
    async def get_stock_by_date(date):
        async def fetch_data():
            pool = await get_db_pool()
            async with pool.acquire() as conn:
                query = "SELECT * FROM stocks WHERE date = $1"
                rows = await conn.fetch(query, date)
            return [dict(row) for row in rows]

        stocks_data = await fetch_data()
        if not stocks_data:
            return jsonify({"message": "Dados não encontrados para o ativo e data informados"}), 404

        return jsonify(stocks_data), 200

    @app.route('/summary/<string:date>', methods=['GET'])
    async def get_summary(date):
        async def fetch_data():
            pool = await get_db_pool()
            async with pool.acquire() as conn:
                query = "SELECT * FROM ibovespa_summary WHERE date = $1"
                rows = await conn.fetch(query, date)
            return [dict(row) for row in rows]

        summary_data = await fetch_data()
        if not summary_data:
            return jsonify({"message": "Dados não encontrados para o ativo e data informados"}), 404

        return jsonify(summary_data), 200

    @app.route('/stocks/<string:ativo>/<string:ano>/<string:mes>', methods=['GET'])
    async def get_stock_data(ativo, ano, mes):
        like_pattern = f"{ano}-{mes.zfill(2)}%"
        print(f"Consulta com LIKE: {like_pattern}")

        async def fetch_data():
            pool = await get_db_pool()
            async with pool.acquire() as conn:
                query = """
                    SELECT val_max, date FROM stocks
                    WHERE ativo = $1
                    AND date LIKE $2
                    ORDER BY date;
                """
                rows = await conn.fetch(query, ativo, like_pattern)
            return rows

        rows_data = await fetch_data()

        if not rows_data:
            return jsonify({"message": "Nenhum dado encontrado para o ativo e período informado"}), 404

        result = [dict(row) for row in rows_data]

        return jsonify({"ativo": ativo, "dados": result}), 200

    return app
