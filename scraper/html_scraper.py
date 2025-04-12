from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

async def scrape_html():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _scrape_html)

def _scrape_html():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/"
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#high tbody tr"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#low tbody tr"))
        )
        return driver.page_source
    finally:
        driver.quit()
