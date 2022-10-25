import os
import json
import requests
from dotenv import load_dotenv

url = 'https://ictbb.crm17.dynamics.com/api/data/v9.1/beembk_moduls'

# get token from .env file
load_dotenv()
bearer_token = os.getenv('BEARER_TOKEN')

nummer = '106'
param = "contains(beembk_modulnummer,\'" + nummer + "\')"

# request url and parse json
# set up utf-8 encoding to avoid errors

headers = {
    'Authorization': 'Bearer ' + bearer_token,
    'content-type': 'application/json',
    }
parameters = {
    '$filter': param
    }

response = requests.get(url, headers=headers, params=parameters)
print(response.status_code)
print(response.text)


