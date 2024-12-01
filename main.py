from src.data_processing.preprocess import preprocess_excel_to_csv
from src.visualizations.dashboard import render_dashboard

raw_file = "data/raw/APT_data-info-dictionary_final.xlsx"
cleaned_file = "data/processed/APT_data_cleaned.csv"

if __name__ == "__main__":
    preprocess_excel_to_csv(raw_file, cleaned_file)
    render_dashboard(cleaned_file)