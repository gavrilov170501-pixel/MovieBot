import requests

from config import KINOPOISK_API_KEY


BASE_URL = "https://kinopoiskapiunofficial.tech/api/v2.2"


def search_movie(query):
    headers = {
        "X-API-KEY": KINOPOISK_API_KEY
    }

    params = {
        "keyword": query
    }

    r = requests.get(
        f"{BASE_URL}/films",
        headers=headers,
        params=params,
        timeout=20
    )

    if r.status_code != 200:
        return None

    data = r.json()

    if not data.get("items"):
        return None

    return data["items"][0]
