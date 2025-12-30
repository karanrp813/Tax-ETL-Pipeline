# Automated Tax Data ETL Pipeline

## Project Overview
Designed for **Federal Tax Advisory (FTA)** workflows, this Python-based ETL pipeline automates the processing of raw financial data for R&D tax credit analysis and asset depreciation schedules. 

It simulates the transition from manual Excel processing to automated data engineering, reducing the risk of human error in tax computations.

## Key Features
* **Automated Data Cleaning:** Ingests raw CSVs, standardizes date formats, and removes duplicate transactions to ensure audit-ready data integrity.
* **R&D Credit Logic:** Implements keyword-based logic (NLP approach) to flag expenses eligible for Federal Research & Development credits.
* **Depreciation Engine:** Automatically calculates Straight-Line depreciation for asset lists, handling mixed-format input data.
* **Excel Reporting:** Outputs a consolidated, multi-tab Excel workbook (`.xlsx`) with an executive summary dashboard for tax managers.

## Tech Stack
* **Python 3.11**
* **Pandas:** For high-volume data manipulation and ETL.
* **OpenPyXL:** For writing formatted Excel reports.
* **NumPy:** For numerical operations.

## Usage
1.  Place raw data in `input_data/`.
2.  Run the pipeline:
    ```bash
    python etl_pipeline.py
    ```
3.  View the generated `EY_Tax_Ready_Report.xlsx` in `output_data/`.