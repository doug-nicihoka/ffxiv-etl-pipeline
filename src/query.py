"""
Query Module.
Provides a Command Line Interface (CLI) to search for items in the local SQLite database.
"""

import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ffxiv.db"


def search_items_by_name(item_name: str) -> list[tuple[int, str]]:
    """
    Searches the database for items whose names partially match the given string.

    Args:
        item_name (str): The partial or full name of the item to search for.

    Returns:
        list[tuple[int, str]]: A list of tuples containing the item ID and name.
    """
    with sqlite3.connect(DB_PATH) as connection:
        result = connection.execute(
            """
            SELECT id, name
            FROM items
            WHERE name LIKE ?
            ORDER BY name ASC
            """,
            (f"%{item_name}%",)
        ).fetchall()

        return result


def main() -> None:
    """
    Parses CLI arguments and executes the search query.
    """
    parser = argparse.ArgumentParser(description="Search FFXIV items in the local database.")

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Search for items by name (partial match)",
    )

    args = parser.parse_args()

    if args.name:
        result = search_items_by_name(args.name)
        
        if result:
            print(*result, sep="\n")
        else:
            print(f"No items found matching '{args.name}'.")


if __name__ == "__main__":
    main()