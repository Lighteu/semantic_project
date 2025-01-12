from src.utils.api_handler import *
from src.config import *
from src.utils.cache_handler import *
import json

def main() :
    with open('data/python-data/ability_pages_list.json', 'r') as file:
        data = json.load(file)
        
    infoboxes_data = []
    for datum in tqdm(data) :
        try :
            wikitext = fetch_page_source(datum['title'])
        except:
            continue
        infobox = None
        infobox = extract_infobox(wikitext, "AbilityInfobox/header")
        if infobox : 
            infoboxes_data.append(
                {
                    'name': datum['title'],
                    'infobox': {param.name.strip(): param.value.strip() for param in infobox.params},
                    'template': "AbilityInfobox/header"
                }
            )
        time.sleep(0.5)
        
                
    with open('data/python-data/infoboxes/ability_infoboxes.json', 'w', encoding='utf-8') as file:
        json.dump(infoboxes_data, file, ensure_ascii=False)
    

if __name__ == '__main__' :
    main()