import json 
from icecream import ic
with open('data/python-data/infoboxes/pokemon_infoboxes.json' , 'r') as f:
    data = json.load(f)
    
temp = {}

for datum in data:
    for field in datum['infobox']:
        if field not in temp:
            temp[field] = datum['infobox'][field]
            
ic(temp)