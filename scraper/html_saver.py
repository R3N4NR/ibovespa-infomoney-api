from bs4 import BeautifulSoup
import os

def update_html_content(original_html, new_data_dict):
    soup = BeautifulSoup(original_html, "html.parser")

    container = soup.find("div", id="novos-dados")
    if not container:
        container = soup.new_tag("div", id="novos-dados")
        soup.body.append(container)

    container.clear()

    for key, value in new_data_dict.items():
        p = soup.new_tag("p")
        p.string = f"{key}: {value}"
        container.append(p)

    return str(soup)

def save_html_to_file(html, file_path="data/pagina.html", new_data=None):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if new_data:
            html = update_html_content(html, new_data)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"HTML salvo com sucesso em {file_path}.")
    except Exception as e:
        print(f"Erro ao salvar o HTML em {file_path}: {e}")
        raise
