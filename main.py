import requests
import xlsxwriter


# Constants
BASE_URL = "https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_modulmappings"
TOKEN_URL = "https://modulbaukasten.ch/assets/auth.php"
ID_INF_PE = '1eac87d6-6d82-eb11-a812-0022486f6f83'
ID_ICT = 'f1e7a970-6f82-eb11-a812-0022486f6f83'
ID_BINF = '03a95323-bf92-eb11-b1ac-000d3a831ef4'

# Cached bearer token
_BEARER_TOKEN = None

# Retrieve bearer token
def get_bearer_token():
    """
    Retrieve bearer token from modulbaukasten.ch API.
    Token is cached after first retrieval.

    Returns:
        Bearer token string in format "Bearer <token>"
    """
    global _BEARER_TOKEN

    if _BEARER_TOKEN is not None:
        return _BEARER_TOKEN

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
    }
    response = requests.get(TOKEN_URL, headers=headers, allow_redirects=True)
    response.raise_for_status()  # Raise error for bad status codes
    token_data = response.json()
    _BEARER_TOKEN = f"{token_data['token_type']} {token_data['access_token']}"
    return _BEARER_TOKEN

# Get all modules
def get_all_modules(identification):
    headers = {
        'Authorization': get_bearer_token(),
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

# Get single module by number
def get_module_by_number(module_number):
    """
    Fetch details for a specific module by its number.

    Args:
        module_number: The module number to search for (e.g., "162")

    Returns:
        A formatted string with module details or an error message
    """
    try:
        # Try all education types to find the module
        for edu_id, edu_name in [(ID_INF_PE, 'Informatiker/in EFZ Plattformentwicklung'),
                                  (ID_ICT, 'ICT-Fachmann/-frau EFZ'),
                                  (ID_BINF, 'Betriebsinformatiker/in EFZ')]:
            response_data = get_all_modules(edu_id)

            # Search for the module
            if 'value' not in response_data:
                continue

            for module in response_data['value']:
                if module.get('beembk_Modul', {}).get('beembk_modulnummer') == str(module_number):
                    # Extract module details
                    modul = module.get('beembk_Modul', {})
                    modulnummer = modul.get('beembk_modulnummer', 'N/A')
                    modultitel = modul.get('beembk_modultitel', 'N/A')
                    kompetenz = modul.get('beembk_kompetenz', 'N/A')
                    lernort = module.get('beembk_Lernort', {}).get('beembk_lernortname', 'N/A')
                    lehrjahr = module.get('beembk_Level', {}).get('beembk_levelname', 'N/A')
                    modultyp = module.get('beembk_Modultyp', {}).get('beembk_modultyp', 'N/A')
                    pdf_name = modul.get('beembk_pdfname_de', '')

                    # Format output
                    output = f"""
# Modul {modulnummer}: {modultitel}

**Bildungsgang:** {edu_name}
**Lernort:** {lernort}
**Lehrjahr gemäss ICT BB:** {lehrjahr}
**Modultyp:** {modultyp}

## Kompetenz
{kompetenz}
"""
                    if pdf_name:
                        pdf_url = f"https://modulbaukasten.ch/Module/{pdf_name}"
                        output += f"\n**PDF:** {pdf_url}\n"

                    return output

        return f"Modul {module_number} nicht gefunden."

    except Exception as e:
        return f"Fehler beim Abrufen des Moduls {module_number}: {str(e)}"

# Main execution
def main():
    # choose education
    response_data = get_all_modules(ID_INF_PE)
    create_markdown_files(response_data)
    create_excel_file(response_data)

if __name__ == "__main__":
    main()
