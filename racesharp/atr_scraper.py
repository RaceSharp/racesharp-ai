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

    races = []

    for link in soup.find_all("a"):

        text = link.get_text(
            strip=True
        )

        if ":" in text:

            races.append(text)

    return races[:50]
