from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
import json
from rdflib import Graph
from tqdm import tqdm
import urllib.parse
from src.utils.html_handler import *

def json_to_rdf(json_list, base_url="http://localhost:3030/bulba_vocab#"):
    """
    Converts a list of JSON data representing Pokémon abilities into RDF format using schema.org vocabulary.

    Args:
        json_list (list): A list of dictionaries containing Pokémon ability data.
        base_url (str): The base URL for Pokémon ability resources.

    Returns:
        str: RDF data in Turtle format.
    """
    # Namespaces
    SCHEMA = Namespace("http://schema.org/")
    BULBA = Namespace(base_url)

    # Create RDF graph
    g = Graph()
    g.bind("schema", SCHEMA)
    g.bind("bulba", BULBA)

    for data in tqdm(json_list):
        # Sanitize URI with URL encoding
        name = data.get("name", "Unknown")
        uri_name = f"{name}"
        ability_uri = URIRef(base_url + urllib.parse.quote(uri_name.replace(" ", "_")))
        g.add((ability_uri, RDF.type, SCHEMA.Thing))
        g.add((ability_uri, RDF.type, URIRef(BULBA.Ability)))

        # Iterate through all keys and add them to the RDF graph
        for key, value in data['infobox'].items():
            if not value:
                continue

            # Handle translations and transliterations
            if key in ["jpname", "jptrans", "jptranslit"]:
                g.add((ability_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
            # Handle general attributes
            elif key in ["name", "gen", "colorscheme"]:
                g.add((ability_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
            # Catch all other keys as additional properties
            else:
                g.add((ability_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))

    # Serialize the graph to Turtle format
    return g.serialize(format="turtle").encode('utf-8')


def main():
    with open('data/python-data/infoboxes/ability_infoboxes.json', 'r') as file:
        data = json.load(file)
    
    rdf_data = json_to_rdf(data)
    print(rdf_data)
    with open('data/python-data/rdf/abilities.ttl', 'wb') as file:
        file.write(rdf_data)
        
if __name__ == '__main__':
    main()