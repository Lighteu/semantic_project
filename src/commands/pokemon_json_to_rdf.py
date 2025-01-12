from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
import json
from rdflib import Graph
from tqdm import tqdm
import urllib.parse
from src.utils.html_handler import *

def json_to_rdf(json_list, base_uri="http://localhost:3030/bulba_vocab#"):
    """
    Converts a list of JSON data representing Pokémon into RDF format using schema.org vocabulary.

    Args:
        json_list (list): A list of dictionaries containing Pokémon data.
        base_uri (str): The base URI for Pokémon resources.

    Returns:
        str: RDF data in Turtle format.
    """
    # Namespaces
    SCHEMA = Namespace("http://schema.org/")
    BULBA = Namespace(base_uri)

    # Create RDF graph
    g = Graph()
    g.bind("schema", SCHEMA)
    g.bind("bulba", BULBA)

    for data in tqdm(json_list):
        name = data.get("name", "Unknown")
        uri_name = f"{name}"  # Append "(Pokémon)" to the name
        pokemon_uri = URIRef(base_uri + urllib.parse.quote(uri_name.replace(" ", "_")))
        g.add((pokemon_uri, RDF.type, SCHEMA.Thing))
        g.add((pokemon_uri, RDF.type, URIRef(BULBA.Pokemon)))

        for key, value in data['infobox'].items():
            if not value:
                continue

            if key.startswith("type") or key.startswith("ability") or key.startswith("form"):
                g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
            elif key.startswith("height"):
                g.add((pokemon_uri, SCHEMA.height, Literal(strip_html_tags(value))))
            elif key.startswith("weight"):
                g.add((pokemon_uri, SCHEMA.weight, Literal(strip_html_tags(value))))
            elif key in ["image","name", "jname", "tmname", "ndex", "category", "color", "friendship", "catchrate", "generation", "gender", "gendercode", "body", "lv100exp", "oldexp"]:
                g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
            elif key.endswith("note"):
                g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
            else:
                g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))

    # Serialize the graph to Turtle format
    return g.serialize(format="turtle").encode('utf-8')


def main():
    with open('data/python-data/infoboxes/pokemon_infoboxes.json', 'r') as file:
        data = json.load(file)
    
    rdf_data = json_to_rdf(data)
    print(rdf_data)
    with open('data/python-data/rdf/pokemons.ttl', 'wb') as file:
        file.write(rdf_data)
        
if __name__ == '__main__':
    main()