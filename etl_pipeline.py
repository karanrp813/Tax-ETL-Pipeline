import pandas as pd
import numpy as np

def clean_expense_data(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    # 1. EXTRACT: Load the raw data
    df = pd.read_csv(input_file)
    initial_count = len(df)
    print(f"Raw data loaded: {initial_count} rows")

    # 2. DATA INTEGRITY: Handle Duplicates & Missing Values
    # EY JD Requirement: "Detect and communicate data-related complexities"
    
    # Check for duplicates based on Transaction_ID
    # keep='first' means we keep the first occurrence and drop the rest.
    duplicates = df[df.duplicated(subset=['Transaction_ID'], keep='first')]
    if not duplicates.empty:
        print(f"ALERT: Found {len(duplicates)} duplicate transactions. Removing them to prevent double-counting.")
        # Actually drop them
        df = df.drop_duplicates(subset=['Transaction_ID'], keep='first')

    # Handle missing Transaction IDs (We cannot audit a transaction without an ID)
    missing_ids = df['Transaction_ID'].isnull().sum()
    if missing_ids > 0:
        print(f"ALERT: Found {missing_ids} rows with missing Transaction IDs. Dropping these rows.")
        df = df.dropna(subset=['Transaction_ID'])

    # 3. TAX LOGIC: R&D Classification (The "Smart" Part)
    # EY JD Requirement: "Configure and calculate client research credits"
    
    # Define keywords that likely indicate R&D activity
    # In a real EY role, this list would be thousands of words long or powered by ML.
    rnd_keywords = ['Prototype', 'Lab', 'Python', 'Cloud', 'Design', 'Test', 'Algorithm']

    # We use a lambda function to scan the 'Description' column.
    # If a keyword is found, set Is_RnD_Eligible to True, else False.
    df['Is_RnD_Eligible'] = df['Description'].apply(
        lambda x: any(keyword.lower() in str(x).lower() for keyword in rnd_keywords)
    )

    # 4. LOAD: Save the clean data
    df.to_csv(output_file, index=False)
    
    final_count = len(df)
    print(f"Data cleaning complete. Saved to {output_file}")
    print(f"Rows retained: {final_count} (Dropped {initial_count - final_count} rows)")
    print("--------------------------------------------------\n")
def process_asset_depreciation(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    # 1. EXTRACT
    df = pd.read_csv(input_file)
    print(f"Asset data loaded: {len(df)} rows")

    # 2. TRANSFORM: Date Standardization (The "Data Complexity" part)
    # EY requires "Attention to detail". Dates are the #1 cause of tax errors.
    # pd.to_datetime is smart enough to figure out "March 10" vs "01/15" automatically.
    # errors='coerce' means if a date is garbage, turn it into NaT (Not a Time) so we can catch it.
    df['Purchase_Date_Normalized'] = pd.to_datetime(df['Purchase_Date'], errors='coerce')

    # Check for invalid dates
    invalid_dates = df['Purchase_Date_Normalized'].isnull().sum()
    if invalid_dates > 0:
        print(f"CRITICAL ERROR: Found {invalid_dates} assets with invalid purchase dates. Please review raw data.")

    # 3. CALCULATION: Straight-Line Depreciation
    # Formula: (Cost - Salvage Value) / Useful Life
    # We assume Salvage Value is $0 for this exercise.
    
    # We create a new column 'Annual_Depreciation'
    # round(..., 2) ensures we stick to 2 decimal places (currency standard).
    df['Annual_Depreciation'] = round(df['Cost'] / df['Useful_Life_Years'], 2)

    # 4. LOAD
    df.to_csv(output_file, index=False)
    
    print(f"Depreciation calculated. Saved to {output_file}")
    # Show a sample calculation to the user
    print(f"Sample Calculation: Asset {df.iloc[0]['Asset_ID']} (Cost ${df.iloc[0]['Cost']}) -> ${df.iloc[0]['Annual_Depreciation']}/year")
    print("--------------------------------------------------\n")

def create_excel_report(expense_file, asset_file, output_excel):
    print(f"--- Generating Final Excel Report: {output_excel} ---")
    
    # Load the processed data
    df_expenses = pd.read_csv(expense_file)
    df_assets = pd.read_csv(asset_file)

    # --- CALCULATE SUMMARY METRICS ---
    # 1. Total R&D Eligible Spend
    # We filter for rows where Is_RnD_Eligible is True, then sum the 'Amount'
    total_rnd_spend = df_expenses[df_expenses['Is_RnD_Eligible'] == True]['Amount'].sum()
    
    # 2. Total Annual Depreciation
    total_depreciation = df_assets['Annual_Depreciation'].sum()

    # Create a simple DataFrame for the Summary Page
    summary_data = {
        'Metric': ['Total R&D Eligible Expenses', 'Total Annual Depreciation', 'Potential Tax Credit (approx 10% of R&D)'],
        'Value': [total_rnd_spend, total_depreciation, total_rnd_spend * 0.10] # Assuming a rough 10% credit rate for demo
    }
    df_summary = pd.DataFrame(summary_data)

    # --- WRITE TO EXCEL ---
    # We use ExcelWriter to create multiple sheets in one file
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
        df_expenses.to_excel(writer, sheet_name='Detailed Expenses', index=False)
        df_assets.to_excel(writer, sheet_name='Asset Schedule', index=False)
    
    print(f"Success! Final report saved to {output_excel}")
    print("--------------------------------------------------\n")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Define file paths
    raw_exp = 'input_data/expenses_raw.csv'
    clean_exp = 'output_data/expenses_cleaned.csv'
    
    raw_asset = 'input_data/assets_raw.csv'
    calc_asset = 'output_data/assets_calculated.csv'
    
    final_report = 'output_data/EY_Tax_Ready_Report.xlsx'

    # 1. Run Expense Cleaning
    clean_expense_data(raw_exp, clean_exp)
    
    # 2. Run Asset Depreciation
    process_asset_depreciation(raw_asset, calc_asset)

    # 3. Generate Final Excel Report
    create_excel_report(clean_exp, calc_asset, final_report)