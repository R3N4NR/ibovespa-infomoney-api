from bs4 import BeautifulSoup
from datetime import datetime
import uuid
def parse_table(table):
    rows = []
    headers = [th.get_text(strip=True) for th in table.select("thead tr th")]

    for tr in table.select("tbody tr"):
        values = [td.get_text(strip=True) for td in tr.select("td")]
        if len(values) != len(headers):
            continue  
        row = dict(zip(headers, values))
        row["Data"] = datetime.now().date().isoformat()
        row["ID"] = uuid.uuid4()
        rows.append(row)
    return rows

def extract_table_data(html):
    soup = BeautifulSoup(html, "html.parser")

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

    return {today: data}

def summary_info(html):
    soup = BeautifulSoup(html, "html.parser")
    line_info = soup.select_one("div.line-info")

    if not line_info:
        return {}

    result = {
        "Date": datetime.now().date().isoformat(),
        "ID": str(uuid.uuid4())
    }

    for div in line_info.find_all("div"):
        label = div.find("label")
        value = div.find("p")
        if label and value:
            label = label.get_text(strip=True)
            value = value.get_text(strip=True)
            result[label] = value
    print(result)
    return result

    
    







