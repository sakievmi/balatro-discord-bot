import json

with open('jokers.json', 'r') as file:
    jokers = json.load(file)

jokers_list = []
for joker_name in jokers:
    joker = jokers[joker_name]

    jokers_list.append(joker)