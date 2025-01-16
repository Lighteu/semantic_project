import json 
from icecream import ic
with open('data/python-data/infoboxes/move_infoboxes.json' , 'r') as f:
    data = json.load(f)
    
temp = {}

for datum in data:
    for field in datum['infobox']:
        if field not in temp.keys():
            temp[field] = datum['infobox'][field]
            
ic(temp)