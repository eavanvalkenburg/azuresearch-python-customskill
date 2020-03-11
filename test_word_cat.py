import requests
import json
import pandas as pd
import pprint

local_url = "http://localhost:7071/api/word_categorizer"
with open("word_categorizer/sample.dat") as json_file:
    data = json.load(json_file)

headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
# headers['Authorization'] = f'Bearer {key}'

resp = requests.post(local_url, headers=headers, json=data)
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(resp.json())