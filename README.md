# 🌐 ICT Crawler
A script to scrape module data from [modulbaukasten.ch](https://modulbaukasten.ch) and save the results in both markdown files and an Excel spreadsheet.

## 🌟 Features
- Retrieves the Modulbeschreibung for ICT Module from [modulbaukasten.ch](https://modulbaukasten.ch)
- Generates individual markdown files for each module with relevant details.
- Downloads related PDFs for the modules.
- Creates an Excel sheet summarizing the module details.

## 🛠️ Prerequisites

You need to have the following libraries installed:

- requests: For making HTTP requests.
- xlsxwriter: For generating Excel files.

Install the required libraries using:
```bash
pip install -r requirements.txt
```

## 🚀 Usage
To run the script:
```bash
python main.py
```
Upon successful execution:

- Markdown files for each module will be created in the current directory.
- PDFs related to the modules will be downloaded to the current directory.
- An Excel sheet named Module_INF-PE.xlsx with the columns 'Modulnummer', 'Modultitel', 'Lernort', 'Lehrjahr' and 'Modultyp' will be generated in the current directory.

## ⚙️ Configuration

The script is set up with predefined constants for API endpoints and identifiers. To customize for different modules or endpoints, adjust the following constants in the main.py script:

- BASE_URL: The base API endpoint for module data.
- TOKEN_URL: The endpoint to retrieve the authentication token.
- ID_INF_PE (Informatiker/in EFZ Fachrichtung Plattformentwicklung), ID_ICT (ICT-Fachmann/-frau EFZ), ID_BINF (Betriebsinformatiker/in EFZ): Identifiers for different educational modules.