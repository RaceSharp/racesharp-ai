import requests


def lookup_race(track, time):

    url = f"https://m.attheraces.com/racecard/{track}/"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        return {
            "track": track,
            "time": time,
            "url": url,
            "status_code": response.status_code,
            "page_length": len(response.text)
        }

    except Exception as e:
        return {
            "track": track,
            "time": time,
            "error": str(e)
        }
