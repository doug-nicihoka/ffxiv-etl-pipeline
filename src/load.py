"""
Load Module.
Responsible for persisting the cleaned FFXIV items into a local SQLite database.
"""

import os
import sqlite3
from typing import Any


def save_items_to_sqlite(cleaned_items: list[dict[str, Any]], db_path: str = "data/ffxiv.db") -> None:
    """
    Creates the database schema if it doesn't exist and inserts/updates the cleaned items.

    Args:
        cleaned_items (list[dict[str, Any]]): The standardized item dictionaries.
        db_path (str): The relative path to the SQLite database file.
    """
    if not cleaned_items:
        print("[LOAD] No items to save. Aborting database operation.")
        return

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"[LOAD] Connecting to database at '{db_path}'...")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                item_level INTEGER NOT NULL,
                rarity INTEGER NOT NULL
            )
        """)

        insert_query = """
            INSERT OR REPLACE INTO items (id, name, item_level, rarity)
            VALUES (:id, :name, :item_level, :rarity)
        """

        cursor.executemany(insert_query, cleaned_items)
        
        print(f"[LOAD] Success! {cursor.rowcount} items saved or updated in the database.")


def main() -> None:
    """
    Tests SQLite funcion with dummy data.
    """
    dummy_data = [
        {"id": 1, "name": "Gil", "item_level": 0, "rarity": 1},
        {"id": 2, "name": "Fire Shard", "item_level": 0, "rarity": 1},
        {"id": 0, "name": "Ghost Item", "item_level": 0, "rarity": 1}
    ]
    
    print("[LOAD] Running standalone test...")
    save_items_to_sqlite(dummy_data)


if __name__ == "__main__":
    main()