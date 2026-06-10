import requests
from bs4 import BeautifulSoup


def get_atr_page():

    url = "https://m.attheraces.com/racecards"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=15
    )

    return {
        "status_code": response.status_code,
        "length": len(response.text)
    }


def get_racecards():

    url = "https://m.attheraces.com/racecards"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=15
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    texts = []

    for tag in soup.find_all(
        ["a", "div", "span"]
    ):

        text = tag.get_text(
            strip=True
        )

        if text and len(text) > 3:
            texts.append(text)

    return texts[:100]
