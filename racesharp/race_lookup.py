import requests
from bs4 import BeautifulSoup


def lookup_race(track, time):

    return {
        "track": track,
        "time": time,
        "status": "live_lookup_pending"
    }
