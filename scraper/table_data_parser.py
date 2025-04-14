from bs4 import BeautifulSoup
from datetime import datetime
import uuid
def parse_table(table):
    rows = []
    headers = [th.get_text(strip=True) for th in table.select("thead tr th")]

    for tr in table.select("tbody tr"):
        values = [td.get_text(strip=True) for td in tr.select("td")]
        if len(values) != len(headers):
            continue  # Ignora linhas com quantidade de dados inconsistentes
        row = dict(zip(headers, values))
        row["Data"] = datetime.now().date().isoformat()
        row["ID"] = uuid.uuid4()
        rows.append(row)
    return rows

def extract_table_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Armazenando a data uma vez no início da função
    today = datetime.now().date().isoformat()

    data = {
        "high_values": [],
        "low_values": []
    }

    high = soup.select_one("table#high")
    low = soup.select_one("table#low")

    if high:
        data["high_values"] = parse_table(high)
    if low:
        data["low_values"] = parse_table(low)

   
    # Organiza os dados com a data no formato iso
    return {today: data}
