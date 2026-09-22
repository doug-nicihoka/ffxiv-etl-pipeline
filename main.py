"""
Main Module.
Responsible for executing the complete ETL pipeline: Extract, Transform, and Load.
"""

import argparse

from src.extract import fetch_ffxiv_items
from src.load import save_items_to_sqlite
from src.transform import clean_ffxiv_items


def run_pipeline(limit: int=100) -> None:
    """
    Executes the FFXIV ETL pipeline step by step, coordinating data flow between modules.
    """
    print("=== Starting FFXIV ETL Pipeline ===")

    # Step 1: Extract
    print("\n[STEP 1] Extracting data...")
    raw_data = fetch_ffxiv_items(limit)

    # Step 2: Transform
    print("\n[STEP 2] Transforming data...")
    cleaned_data = clean_ffxiv_items(raw_data)

    # Step 3: Load
    print("\n[STEP 3] Loading data into database...")
    save_items_to_sqlite(cleaned_data)

    print("\n=== Pipeline Execution Completed ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int, default=100,
                        help="Set the maximum number of items to be fetched from API. Default = 100")
    args = parser.parse_args()

    run_pipeline(args.limit)