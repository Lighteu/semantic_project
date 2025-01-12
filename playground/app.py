import requests
import time
import pickle
import logging
from icecream import ic
import json
from tqdm import tqdm
from config import *

# Constants
API_URL = "https://bulbapedia.bulbagarden.net/w/api.php"
HEADERS = {
    "User-Agent": "Mounir Rouibi from University Jean Monnet (mohamed.rouibi@etu.univ-st-etienne.fr)"
}

# Logging setup
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Save and load cache
def save_cache(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_cache(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Log requests
def log_request(endpoint, params):
    logging.info(f"Request to {endpoint} with params: {params}")

# Handle API requests with retries and throttling
def make_request(params, retries=3):
    for i in range(retries):
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.headers.get("MediaWiki-API-Error") == "maxlag":
            print(f"Maxlag error. Retrying in {2 ** i} seconds...")
            time.sleep(2 ** i)  # Exponential backoff
        else:
            response.raise_for_status()  # Raise other HTTP errors
    raise Exception("Failed to fetch data after retries")

# Fetch all pages in the namespace
def fetch_all_pages():
    params = {
        "action": "query",
        "list": "allpages",
        "apnamespace": 0,
        "aplimit": 50,  # Fetch 50 pages at a time
        "format": "json"
    }

    pages = []
    while True:
        log_request(API_URL, params)
        response = make_request(params)
        pages.extend(response["query"]["allpages"])
        if "continue" not in response:
            break
        params["apcontinue"] = response["continue"]["apcontinue"]
        time.sleep(0.5)  # Throttle requests

    return pages

# Fetch specific page source wikitext
def fetch_page_source(page_title):
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "wikitext",
        "format": "json"
    }

    log_request(API_URL, params)
    response = make_request(params)
    return response["parse"]["wikitext"]["*"]

# Extract infobox from wikitext
def extract_infobox(wikitext, template_name):
    import mwparserfromhell
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if template.name.matches(template_name):
            return template
    return None

def fetch_pages_with_infobox():
    """
    Fetch pages that include any of the templates from the famous_templates list.
    """
    filtered_pages = []

    for template in tqdm(famous_templates):
        params = {
            "action": "query",
            "list": "embeddedin",
            "eititle": f"Template:{template}",
            "eilimit": 50,  # Fetch 50 pages at a time
            "eifilterredir": "nonredirects",  # Ignore redirects
            "format": "json"
        }

        while True:
            log_request(API_URL, params)
            try:
                response = make_request(params)
            except:
                break
            if "query" in response and "embeddedin" in response["query"]:
                filtered_pages.extend(response["query"]["embeddedin"])
            
            # Continue pagination
            if "continue" not in response:
                break
            params.update(response["continue"])
            time.sleep(0.5)  # Throttle requests

    return filtered_pages

# Main process
if __name__ == "__main__":
    # Load cached pages or fetch new
    """ pages = load_cache("pages_cache.pkl")
    if not pages :
        exit
    if not pages:
        pages = fetch_all_pages()
        save_cache("pages_cache.pkl", pages)

    print(f"Total pages fetched: {len(pages)}") """

    # Load cached pages or fetch new
    """ pages_with_infobox = load_cache("pages_with_infobox_cache.pkl")
    if not pages_with_infobox :
        exit
    if not pages_with_infobox: """
    pages_with_infobox = fetch_pages_with_infobox()
    save_cache("pages_with_infobox_cache.pkl", pages_with_infobox)

    print(f"Total pages_with_infobox fetched: {len(pages_with_infobox)}")
    
    infoboxes_data = []
    for page in tqdm(pages_with_infobox) :
        wikitext = fetch_page_source(page['title'])
        infobox = None
        for template in famous_templates:
            infobox = extract_infobox(wikitext, template)
            if infobox : 
                infoboxes_data.append(
                    {
                        'name': page['title'],
                        'infobox': {param.name.strip(): param.value.strip() for param in infobox.params},
                        'template': template
                    }
                )
        time.sleep(0.5)
                
    with open('infoboxes.json', 'w', encoding='utf-8') as file:
        json.dump(infoboxes_data, file, ensure_ascii=False)
    

