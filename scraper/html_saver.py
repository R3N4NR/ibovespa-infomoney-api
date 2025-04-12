import os

def save_html_to_file(html, file_path="data/pagina.html"):
    """
    Salva o HTML bruto da página em um arquivo local.

    Parâmetros:
    - html (str): Conteúdo HTML capturado via Selenium.
    - file_path (str): Caminho onde o arquivo será salvo. Padrão é 'data/pagina.html'.

    Exceções:
    - Ocorre uma falha ao salvar o arquivo, como um erro de permissão ou falha no sistema de arquivos.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML salvo com sucesso em {file_path}.")
    except Exception as e:
        print(f"Erro ao salvar o HTML em {file_path}: {e}")
        raise
