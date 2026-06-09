import requests
from bs4 import BeautifulSoup


def lookup_race(track, time):

    url = f"https://m.attheraces.com/racecard/{track}/"

    return {
        "track": track,
        "time": time,
        "source": url
    }
