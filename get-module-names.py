import os
import codecs
import requests
from dotenv import load_dotenv

url = 'https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_moduls'

# get token from .env file
load_dotenv()
bearer_token = os.getenv('BEARER_TOKEN')

# TODO: add loop to get multiple modules

def get_module_names(number):
    param = "contains(beembk_modulnummer,\'" + number + "\')"
    headers = {
        'Authorization': bearer_token,
        'content-type': 'application/json',
        'Accept': '*/*'
        'rtert'
        }
    parameters = {
        '$filter': param
        }
    response = requests.request("GET", url, headers=headers, params=parameters)
    json_data = response.json()
    return json_data['value'][0]['beembk_modultitel']


# get module numbers from file
module_number_file = open("modulnummer.txt", "r")
module_number_list= module_number_file.readlines()
module_number_file.close()
module_number_list = [x.strip() for x in module_number_list]

module_name_file = codecs.open("modulnamen.txt", "w", "utf-8")
for module_number in module_number_list:
    module_number = module_number.strip()
    module_name = get_module_names(module_number)
    module_name_file.write(module_name + "\n")
module_name_file.close()