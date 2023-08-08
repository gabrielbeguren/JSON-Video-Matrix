import requests
import json
import os

#This script fills with info the data/data.json file, for testing

url = "https://pokeapi.co/api/v2/pokemon/pikachu"

response = requests.get(url)

if response.status_code == 200:
    new_data = response.json()

    with open('data/data.json', 'r') as json_file:
        existing_data = json.load(json_file)

    if 'data' not in existing_data:
        existing_data['data'] = []  

    existing_data['data'].append(new_data)

    with open('data/data.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)

    print("Data inserted on data/data.json")
else:
    print("(!) Error: ", response.status_code)

