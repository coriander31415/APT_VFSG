# APT_VFSG


## Data
This project uses raw data stored in the `data/raw/` directory. Specifically:
- `APT_data-info-dictionary_final.xlsx`: This is the source file provided by the client. It is not modified and serves as the base for generating the processed CSV file.

The processed data is generated and stored in `data/processed/`.

The processed CSV file is versioned in this repository to avoid frequent regeneration unless the source file is updated.

## Installation and Usage

Follow these steps to set up and run the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository.git
   cd repository

2.	Create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3.	Install required dependencies:
pip install -r requirements.txt

4. 	Run the project:
python3 main.py

5.	(Optional) If you need to deactivate the virtual environment:
  deactivate
