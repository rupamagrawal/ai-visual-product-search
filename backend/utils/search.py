import os

import requests
from dotenv import load_dotenv


load_dotenv()


def search_products(query: str, max_results: int = 12):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return []

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params={
                "engine": "google_shopping",
                "q": query,
                "api_key": api_key,
                "gl": "us",
                "hl": "en",
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return []

    if payload.get("error"):
        return []

    items = []
    for item in payload.get("shopping_results", [])[:max_results]:
        items.append(
            {
                "title": item.get("title"),
                "image": item.get("thumbnail") or item.get("serpapi_thumbnail"),
                "link": item.get("product_link") or item.get("link"),
                "price": item.get("price"),
                "source": item.get("source"),
            }
        )

    return items
