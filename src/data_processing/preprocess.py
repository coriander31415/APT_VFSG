import pandas as pd
import os
from datetime import datetime

input_file = "data/raw/APT_data-info-dictionary_final.xlsx"
output_file = "data/processed/APT_data.csv"

def is_csv_up_to_date(input_file, output_file):
    """
    Check if the processed CSV file is up-to-date compared to the raw Excel file.
    """
    if not os.path.exists(output_file):
        return False

    input_mtime = os.path.getmtime(input_file)
    output_mtime = os.path.getmtime(output_file)
    if output_mtime <= input_mtime:
        return False
    try:
        processed_data = pd.read_csv(output_file)
        required_columns = ['Date', 'Region', 'Country', 'Indicator', 'Input']
        if not all(col in processed_data.columns for col in required_columns):
            return False
    except Exception:
        return False

    return True

def preprocess_excel_to_csv(input_file, output_file, sheet_name=0, date_col='Date', category_cols=None, map_input=None):
    """
    Preprocess the XLSX file and save the cleaned data as a CSV file.
    """
    if category_cols is None:
        category_cols = ['Region', 'Country', 'Indicator', 'Input']
    if map_input is None:
        map_input = {'Yes': 1, 'No': 0, 'Partially': 0.5}

    if not is_csv_up_to_date(input_file, output_file):
        print("Processing Excel file and converting to cleaned CSV...")
        
        data = pd.read_excel(input_file, sheet_name=sheet_name)

        # Preprocess data
        if date_col in data.columns:
            data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
        for col in category_cols:
            if col in data.columns:
                data[col] = data[col].astype('category')
        if 'Input' in data.columns:
            data['Input'] = data['Input'].map(map_input)

        # Save data
        data.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
    else:
        print("Cleaned CSV is up-to-date. No processing needed.")