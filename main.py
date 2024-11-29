from src.data_processing.preprocess import preprocess_excel_to_csv
from src.visualizations.dashboard import render_dashboard

# File paths
raw_file = "data/raw/APT_data-info-dictionary_final.xlsx"
cleaned_file = "data/processed/APT_data_cleaned.csv"

if __name__ == "__main__":
    # Preprocess the XLSX file and save it as a cleaned CSV
    preprocess_excel_to_csv(raw_file, cleaned_file)

    # Render the dashboard to an HTML file
    render_dashboard(cleaned_file)