import pandas as pd
import numpy as np
import os

# Ensure the input directory exists
input_dir = 'input_data'
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

# --- DATASET 1: R&D EXPENSES (The "Messy" File) ---
# We need to test if your pipeline can find "research" keywords.
expense_data = {
    'Transaction_ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004', 'TXN005', 'TXN002', np.nan, 'TXN006'], # Note the duplicate TXN002 and missing ID
    'Date': ['2025-01-10', '2025-01-12', '2025-01-15', '2025-02-01', '2025-02-20', '2025-01-12', '2025-03-05', '2025-03-10'],
    'Description': [
        'AWS Cloud Server for Prototype Hosting',  # Eligible
        'Team Lunch at Chipotle',                  # Non-Eligible
        'Python Scripting for Data Analysis',      # Eligible
        'Marketing Brochure Printing',             # Non-Eligible
        'Lab Equipment - Oscilloscope',            # Eligible
        'Team Lunch at Chipotle',                  # DUPLICATE ROW (Non-Eligible)
        'Consulting Fee for UX Design',            # Eligible
        'Client Dinner'                            # Non-Eligible
    ],
    'Amount': [1500.00, 45.50, 3200.00, 150.00, 12000.00, 45.50, 5000.00, 200.00],
    'Department': ['IT', 'HR', 'IT', 'Sales', 'Engineering', 'HR', 'Design', 'Sales']
}

df_expenses = pd.DataFrame(expense_data)
# Save to CSV
df_expenses.to_csv(f'{input_dir}/expenses_raw.csv', index=False)
print(f"Created {input_dir}/expenses_raw.csv")

# --- DATASET 2: ASSET LIST (For Depreciation) ---
# We need to calculate depreciation, but the dates might be messy.
asset_data = {
    'Asset_ID': ['A100', 'A101', 'A102', 'A103'],
    'Asset_Type': ['Laptop', 'Server', 'Office Chair', '3D Printer'],
    'Purchase_Date': ['01/15/2024', '2024-02-20', 'March 10, 2024', '2024-05-01'], # Mixed date formats!
    'Cost': [1200, 50000, 300, 2500],
    'Useful_Life_Years': [5, 5, 7, 5] # Standard tax life years (MACRS often uses 5 or 7)
}

df_assets = pd.DataFrame(asset_data)
# Save to CSV
df_assets.to_csv(f'{input_dir}/assets_raw.csv', index=False)
print(f"Created {input_dir}/assets_raw.csv")