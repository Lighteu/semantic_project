import json
from rdflib import Graph
from tqdm import tqdm

# JSON-LD context mapping fields to appropriate schema.org IRIs
CONTEXT = {
    "@context": {
        "name": "http://schema.org/name",
        "jname": "http://schema.org/alternateName",
        "tmname": "http://schema.org/alternateName",
        "category": "http://schema.org/category",
        "ndex": "http://schema.org/identifier",
        "forme": "http://schema.org/variantOf",
        "form1": "http://schema.org/alternateName",
        "form2": "http://schema.org/alternateName",
        "form3": "http://schema.org/alternateName",
        "image2": "http://schema.org/image",
        "image3": "http://schema.org/image",
        "type1": "http://schema.org/category",
        "type2": "http://schema.org/category",
        "form3type1": "http://schema.org/category",
        "form3type2": "http://schema.org/category",
        "form2type1": "http://schema.org/category",
        "form2type2": "http://schema.org/category",
        "abilitylayout": "http://schema.org/position",
        "ability1": "http://schema.org/knows",
        "ability2": "http://schema.org/knows",
        "ability2-1": "http://schema.org/knows",
        "ability2-2": "http://schema.org/knows",
        "abilityd": "http://schema.org/knows",
        "abilitycold": "http://schema.org/knows",
        "abilityold": "http://schema.org/knows",
        "abilityoldcaption": "http://schema.org/description",
        "gendercode": "http://schema.org/identifier",
        "catchrate": "http://schema.org/identifier",
        "egggroupn": "http://schema.org/identifier",
        "egggroup1": "http://schema.org/category",
        "egggroup2": "http://schema.org/category",
        "eggcycles": "http://schema.org/identifier",
        "height-ftin": "http://schema.org/height",
        "height-m": "http://schema.org/height",
        "height-ftin2": "http://schema.org/height",
        "height-m2": "http://schema.org/height",
        "height-ftin3": "http://schema.org/height",
        "height-m3": "http://schema.org/height",
        "weight-lbs": "http://schema.org/weight",
        "weight-kg": "http://schema.org/weight",
        "weight-lbs2": "http://schema.org/weight",
        "weight-kg2": "http://schema.org/weight",
        "weight-lbs3": "http://schema.org/weight",
        "weight-kg3": "http://schema.org/weight",
        "mega": "http://schema.org/alternateName",
        "generation": "http://schema.org/identifier",
        "expyield": "http://schema.org/identifier",
        "oldexp": "http://schema.org/identifier",
        "lv100exp": "http://schema.org/identifier",
        "evforms": "http://schema.org/identifier",
        "evtotal": "http://schema.org/identifier",
        "evde": "http://schema.org/identifier",
        "evat2": "http://schema.org/identifier",
        "body": "http://schema.org/category",
        "formbody": "http://schema.org/category",
        "color": "http://schema.org/color",
        "friendship": "http://schema.org/identifier",
        "pokefordex": "http://schema.org/identifier",
        "nocat": "http://schema.org/category"
    }
}

def json_to_rdf(data_list):
    """
    Transforms a list of JSON data into RDF using JSON-LD context.

    Args:
        data_list (list): List of JSON-like data.

    Returns:
        str: RDF serialization in Turtle format for all data.
    """
    graph = Graph()

    for data in tqdm(data_list):
        # Add context to each data entry
        data_with_context = {
            "@context": CONTEXT["@context"],
            **data['infobox']
        }
        # Parse JSON-LD into the RDF graph
        graph.parse(data=json.dumps(data_with_context), format="json-ld")

    # Serialize RDF to Turtle
    return graph.serialize(format="turtle").encode("utf-8")

def main():
    with open('data/python-data/pokemon_infoboxes.json', 'r') as file:
        data = json.load(file)
    
    rdf_data = json_to_rdf(data)
    print(rdf_data)
    with open('data/python-data/rdf/pokemons.ttl', 'wb') as file:
        file.write(json_to_rdf(data))
        
if __name__ == '__main__':
    main()