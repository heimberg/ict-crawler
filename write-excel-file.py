import requests
import json
import xlsxwriter
import win32com.client as win32
import pathlib

token_url = "https://modulbaukasten.ch/assets/auth.php"
modules_url = "https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_modulmappings"

response = requests.request("GET", token_url)
# extract token from response
token = response.text[91:-4]
token = "Bearer " + token

BEARER_TOKEN = token
ID_INF_PE = '1eac87d6-6d82-eb11-a812-0022486f6f83'

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

    response = requests.request("GET", modules_url, headers=headers, params=parameters)

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


workbook = xlsxwriter.Workbook('Module_INF-PE.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'Modulnummer', bold)
worksheet.write('B1', 'Modultitel', bold)
worksheet.write('C1', 'Lernort', bold)
worksheet.write('D1', 'Lehrjahr gem. ICT BB', bold)

for row, data in enumerate(module_numbers):
    worksheet.write_number(row+1, 0, int(data))
for row, data in enumerate(module_names):
    worksheet.write(row+1, 1, data)
for row, data in enumerate(module_lernort):
    worksheet.write(row+1, 2, data)
for row, data in enumerate(module_lehrjahr):
    worksheet.write(row+1, 3, data)
workbook.close()

excel = win32.gencache.EnsureDispatch('Excel.Application')
path = pathlib.Path().resolve()
file = str(path) + '\\Module_INF-PE.xlsx'
wb = excel.Workbooks.Open(file)
ws = wb.Worksheets("Sheet1")
ws.Columns.AutoFit()
wb.Save()
excel.Application.Quit()