import requests


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
