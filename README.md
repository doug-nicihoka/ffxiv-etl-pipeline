# FFXIV ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Native-lightgrey.svg)
![Data Engineering](https://img.shields.io/badge/Data%20Engineering-ETL-success.svg)

## Overview

This project is an ETL pipeline that extracts item data from the public **XIVAPI** (Final Fantasy XIV), transforms the data, and stores it in a local **SQLite** database.

It was built as a portfolio project to practice API integration.

## Architecture & Data Flow

The pipeline is split into separate modules for each ETL step:

1. **Extract (`src/extract.py`):** Connects to the XIVAPI v2 using HTTP requests and fetches item data as JSON. It also handles request timeouts and HTTP errors.
2. **Transform (`src/transform.py`):** Cleans the extracted data, filters out invalid records (such as developer ghost items), selects the relevant fields (ID, Name, Item Level, Rarity), and standardizes strings.
3. **Load (`src/load.py`):** Connects to the local SQLite database, creates the table if needed, and inserts the data using `INSERT OR REPLACE` to avoid duplicate records.
4. **Orchestrator (`main.py`):** Runs the ETL steps in order.

## Project Structure

```text
ffxiv-etl-pipeline/
├── data/
│   └── ffxiv.db            # SQLite database generated after running the pipeline
├── src/
│   ├── extract.py          # Data extraction logic
│   ├── transform.py        # Data cleaning and formatting logic
│   └── load.py             # Database persistence logic
├── .gitignore              # Ignores virtual environments, cache, and database files
├── main.py                 # Pipeline orchestrator
├── requirements.txt        # Python dependencies (requests)
└── README.md               # Project documentation
```
