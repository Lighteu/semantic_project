from src.utils.api_handler import *
from src.utils.cache_handler import *
import json

def main() :
    pages = load_cache("pages_cache.pkl")
    if not pages:
        pages = fetch_all_pages()
        save_cache("pages_cache.pkl", pages)

    print(f"Total pages fetched: {len(pages)}")
    pokemons_pages_list = []
    for page in pages:
        if '(move)' in page['title'].lower() :
            pokemons_pages_list.append(page)
            
    with open('data/python-data/move_pages_list.json', 'w', encoding='utf-8') as file:
        json.dump(pokemons_pages_list, file, ensure_ascii=False)
        
        
if __name__ == '__main__' :
    main()