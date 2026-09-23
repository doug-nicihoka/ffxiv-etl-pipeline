"""
Transform Module.
Responsible for cleaning and standardizing the raw JSON data fetched from the XIVAPI.
"""

from typing import Any


def clean_ffxiv_items(raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Filters raw FFXIV item data, extracting only the essential fields for the database.

    Args:
        raw_items (list[dict[str, Any]]): The raw JSON payload returned by extract.py.

    Returns:
        list[dict[str, Any]]: A list of standardized dictionaries ready for database insertion.
    """
    cleaned_items = []

    for raw_row in raw_items:
        item_id = raw_row.get("row_id")
        fields = raw_row.get("fields", {})

        name = fields.get("Name")
        
        if item_id is None or not name:
            continue

        cleaned_item = {
            "id": item_id,
            "name": name.strip(),
            "item_level": fields.get("LevelItem", 0),
            "rarity": fields.get("Rarity", 1)
        }
        
        cleaned_items.append(cleaned_item)

    return cleaned_items


def main() -> None:
    """
    Tests cleaned data functionality by printing first 3 items.
    """
    from extract import fetch_ffxiv_items
    
    print("[TRANSFORM] Fetching raw data for standalone test...")
    raw_data = fetch_ffxiv_items(limit=3)
    
    cleaned_data = clean_ffxiv_items(raw_data)
    
    print("\n[TRANSFORM] Cleaned Output:")
    for item in cleaned_data:
        print(item)


if __name__ == "__main__":
    main()