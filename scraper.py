import requests
from bs4 import BeautifulSoup


def scrape_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ")