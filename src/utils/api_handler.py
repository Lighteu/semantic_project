import requests
import time
from tqdm import tqdm
from src.config import *
import mwparserfromhell


# Handle API requests with retries and throttling
def make_request(params, retries=3):
    for i in range(retries):
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.headers.get("MediaWiki-API-Error") == "maxlag":
            print(f"Maxlag error. Retrying in {2 ** i} seconds...")
            time.sleep(2 ** i)  
        else:
            response.raise_for_status()  
    raise Exception("Failed to fetch data after retries")

# Fetch all pages in the namespace
def fetch_all_pages():
    params = {
        "action": "query",
        "list": "allpages",
        "apnamespace": 0,
        "aplimit": 50,  
        "format": "json"
    }

    pages = []
    while True:
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

    response = make_request(params)
    return response["parse"]["wikitext"]["*"]

# Extract infobox from wikitext
def extract_infobox(wikitext, template_name):
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