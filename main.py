from src.data_processing.preprocess import preprocess_excel_to_csv

# File paths
raw_file = "data/raw/APT_data-info-dictionary_final.xlsx"
cleaned_file = "data/processed/APT_data_cleaned.csv"

if __name__ == "__main__":
    # Preprocess the XLSX file and save it as a cleaned CSV
    preprocess_excel_to_csv(raw_file, cleaned_file)