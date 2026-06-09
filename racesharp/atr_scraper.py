import requests
from bs4 import BeautifulSoup


def get_atr_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    return response.text
