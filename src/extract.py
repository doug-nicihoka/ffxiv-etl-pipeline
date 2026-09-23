"""
Extract Module.
Responsible for communicating with the XIVAPI v2 and fetching raw item data via HTTP requests.
"""

from typing import Any  # noqa: I001
import requests

XIVAPI_BASE_URL = "https://v2.xivapi.com/api/sheet/Item"


def fetch_ffxiv_items(limit: int = 50) -> list[dict[str, Any]]:
    """
    Fetches a list of Final Fantasy XIV items via XIVAPI v2.

    Args:
        limit (int): The number of items to fetch per request.

    Returns:
        list[dict[str, Any]]: A list containing the raw items as Python dictionaries.
    """
    params = {
        "limit": limit,
    }

    headers = {
        "User-Agent": "FFXIV-ETL-Pipeline/1.0",
        "Accept": "application/json",
    }

    print(f"[EXTRACT] Fetching {limit} items from {XIVAPI_BASE_URL}...")

    try:
        response = requests.get(
            XIVAPI_BASE_URL,
            params=params,
            headers=headers,
            timeout=10,
        )
        
        response.raise_for_status()

        data = response.json()
        rows = data.get("rows", [])

        print(f"[EXTRACT] Success! {len(rows)} raw items received.")
        return rows

    except requests.exceptions.Timeout:
        print("[EXTRACT ERROR] The request timed out (10s limit).")
        raise
    except requests.exceptions.HTTPError as http_err:
        print(f"[EXTRACT ERROR] HTTP error returned by the API: {http_err}")
        raise
    except requests.exceptions.RequestException as err:
        print(f"[EXTRACT ERROR] General network connection failure: {err}")
        raise


def main() -> None:
    """
    Tests extract function by printing first received item.
    """
    test_items = fetch_ffxiv_items(limit=3)

    if test_items:
        print("\nExample of the first received item:")
        
        first_item = test_items[0]
        print(f"ID: {first_item.get('row_id')}")
        print(f"Available fields: {list(first_item.get('fields', {}).keys())[:10]}...")


if __name__ == "__main__":
    main()