import json
import os

data = None
with open('database.json', 'r') as file:
    if os.path.getsize('database.json') == 0:
        data = {}
    else:
        data = json.load(file)

def save():
    with open('database.json', 'w') as f:
        json.dump(data, f)