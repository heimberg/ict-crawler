import os
from webbrowser import get
import requests
from dotenv import load_dotenv
import json

url = "https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_modulmappings"
token_url = "https://modulbaukasten.ch/assets/auth.php"
ID_INF_PE = '1eac87d6-6d82-eb11-a812-0022486f6f83'

response = requests.request("GET", token_url)
# extract token from response
token = response.text[91:-4]
token = "Bearer " + token

BEARER_TOKEN = token

def get_all_modules(identification):
    headers = {
        'Authorization': BEARER_TOKEN,
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    parameter_value = "beembk_Abschluss/beembk_abschlussid eq \'" + identification + "\'"
    parameters = {
        '$filter': parameter_value,
        '$expand': 'beembk_Lernort,beembk_Modul,beembk_Modultyp,beembk_Level'
    }

    response = requests.request("GET", url, headers=headers, params=parameters)

    return response.json()

response = get_all_modules(ID_INF_PE)
# serialize response
json_data = json.dumps(response, indent=4)
# convert json to dict
response_as_dict = json.loads(json_data)

# create list of values for specific key
def get_data(data, search_key, data_list = None):
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

module_numbers = get_data(response_as_dict, 'beembk_modulnummer')

module_names = get_data(response_as_dict, 'beembk_modultitel')

module_kompetenz = get_data(response_as_dict, 'beembk_kompetenz')

module_lernort = get_data(response_as_dict, 'beembk_lernortname')

module_lehrjahr = get_data(response_as_dict, 'beembk_levelname')
print(module_lehrjahr)

# path for the file is https://modulbaukasten.ch/Module/<module_pdf>
module_pdf = get_data(response_as_dict, 'beembk_pdfname_de')

for (number, name, kompetenz, lernort, lehrjahr) in zip(module_numbers, module_names, module_kompetenz, module_lernort, module_lehrjahr):
    # create folders for each module
    # os.mkdir(os.path.dirname(__file__) + '\\' + number + ' ' + name)

    # create file for each module
    with open(number + " " + name + ".md", 'w', encoding="utf-8") as f:
        f.write("#infpe" + '\n' + "Lernort: " + lernort + '\n' + '\n' "Lehrjahr gemäss ICT BB: " + lehrjahr + '\n' + '\n' + "Kompetenz: " + kompetenz + '\n')

## download pdfs
for pdf in module_pdf:
    pdf_url = "https://modulbaukasten.ch/Module/" + pdf
    pdf_name = pdf.split('/')[-1]
    # download pdfs
    with open(pdf_name, 'wb') as f:
        f.write(requests.get(pdf_url).content)
