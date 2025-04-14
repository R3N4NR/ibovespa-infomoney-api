import os

def save_html_to_file(html, file_path="data/pagina.html"):

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML salvo com sucesso em {file_path}.")
    except Exception as e:
        print(f"Erro ao salvar o HTML em {file_path}: {e}")
        raise
