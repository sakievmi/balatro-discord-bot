import json
import os

data = None
with open('json/database.json', 'r') as file:
    if os.path.getsize('json/database.json') == 0:
        data = {}
    else:
        data = json.load(file)

def save():
    with open('json/database.json', 'w') as f:
        json.dump(data, f)