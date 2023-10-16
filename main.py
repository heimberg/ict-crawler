import requests
import xlsxwriter


# Constants
BASE_URL = "https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_modulmappings"
TOKEN_URL = "https://modulbaukasten.ch/assets/auth.php"
ID_INF_PE = '1eac87d6-6d82-eb11-a812-0022486f6f83'
ID_ICT = 'f1e7a970-6f82-eb11-a812-0022486f6f83'
ID_BINF = '03a95323-bf92-eb11-b1ac-000d3a831ef4'

# Retrieve bearer token
def get_bearer_token():
    response = requests.get(TOKEN_URL)
    token = response.text[91:-4]
    return f"Bearer {token}"

BEARER_TOKEN = get_bearer_token()

# Get all modules
def get_all_modules(identification):
    headers = {
        'Authorization': BEARER_TOKEN,
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    parameter_value = f"beembk_Abschluss/beembk_abschlussid eq '{identification}'"
    parameters = {
        '$filter': parameter_value,
        '$expand': 'beembk_Lernort,beembk_Modul,beembk_Modultyp,beembk_Level'
    }
    response = requests.get(BASE_URL, headers=headers, params=parameters)
    return response.json()

# Extract data
def get_data(data, search_key, data_list=None):
    if data_list is None:
        data_list = []
    for key, value in data.items():
        if key == search_key:
            data_list.append(value)
        if isinstance(value, dict):
            get_data(value, search_key, data_list)
        elif isinstance(value, list):
            for item in value:
                get_data(item, search_key, data_list)
    return data_list

# Create markdown files
def create_markdown_files(response_data):
    module_numbers = get_data(response_data, 'beembk_modulnummer')
    module_names = get_data(response_data, 'beembk_modultitel')
    module_kompetenz = get_data(response_data, 'beembk_kompetenz')
    module_lernort = get_data(response_data, 'beembk_lernortname')
    module_lehrjahr = get_data(response_data, 'beembk_levelname')
    module_pdf = get_data(response_data, 'beembk_pdfname_de')

    for (number, name, kompetenz, lernort, lehrjahr) in zip(module_numbers, module_names, module_kompetenz, module_lernort, module_lehrjahr):
        with open(f"{number} {name}.md", 'w', encoding="utf-8") as f:
            f.write(f"#infpe\nLernort: {lernort}\n\nLehrjahr gemäss ICT BB: {lehrjahr}\n\nKompetenz: {kompetenz}\n")

    # Download PDFs
    for pdf in module_pdf:
        pdf_url = f"https://modulbaukasten.ch/Module/{pdf}"
        pdf_name = pdf.split('/')[-1]
        with open(pdf_name, 'wb') as f:
            f.write(requests.get(pdf_url).content)

# Create excel file
def create_excel_file(response_data):
    module_numbers = get_data(response_data, 'beembk_modulnummer')
    module_names = get_data(response_data, 'beembk_modultitel')
    module_lernort = get_data(response_data, 'beembk_lernortname')
    module_lehrjahr = get_data(response_data, 'beembk_levelname')
    module_typ = get_data(response_data, 'beembk_modultyp')

    workbook = xlsxwriter.Workbook('Module_INF-PE.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    headers = ['Modulnummer', 'Modultitel', 'Lernort', 'Lehrjahr gem. ICT BB', 'Modultyp']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, bold)

    for row, data in enumerate(module_numbers):
        try:
            worksheet.write_number(row+1, 0, int(data))
        except:
            worksheet.write(row+1, 0, data)
    for row, data in enumerate(module_names):
        worksheet.write(row+1, 1, data)
    for row, data in enumerate(module_lernort):
        worksheet.write(row+1, 2, data)
    for row, data in enumerate(module_lehrjahr):
        worksheet.write(row+1, 3, data)
    for row, data in enumerate(module_typ):
        worksheet.write(row+1, 4, data)
    
    workbook.close()

# Main execution
def main():
    # choose education
    response_data = get_all_modules(ID_INF_PE)
    create_markdown_files(response_data)
    create_excel_file(response_data)

main()
