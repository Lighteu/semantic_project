from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF
import json
import urllib.parse
from tqdm import tqdm
from src.utils.html_handler import *

def load_abilities(base_uri):
    """Load ability names and map them to their URIs."""
    abilities_graph = Graph()
    abilities_graph.parse('data/python-data/rdf/abilities.ttl', format='turtle', encoding='utf-8')
    ability_map = {}

    for ability in abilities_graph.subjects(RDF.type, URIRef(base_uri + 'Ability')):
        # Extract the readable name from the URI
        ability_name = str(ability).split("#")[-1].split("_%28")[0].replace("_", " ").lower()
        ability_map[ability_name] = ability

    return ability_map

def json_to_rdf(json_list, base_uri="http://localhost:3030/bulba_vocab#"):
    """Generate RDF with proper ability linking."""
    SCHEMA = Namespace("http://schema.org/")
    BULBA = Namespace(base_uri)

    g = Graph()
    g.bind("schema", SCHEMA)
    g.bind("bulba", BULBA)

    # Load ability mappings
    ability_map = load_abilities(base_uri)

    for data in tqdm(json_list):
        name = data.get("name", "Unknown")
        pokemon_uri = URIRef(base_uri + urllib.parse.quote(name.replace(" ", "_")))
        g.add((pokemon_uri, RDF.type, SCHEMA.Thing))
        g.add((pokemon_uri, RDF.type, BULBA.Pokemon))

        for key, value in data['infobox'].items():
            if not value:
                continue

            clean_value = strip_html_tags(value).strip().lower().replace("_", " ")

            # Link ability fields to their URIs
            if key.startswith("ability"):
                ability_uri = ability_map.get(clean_value)
                if ability_uri:
                    g.add((pokemon_uri, BULBA[key], ability_uri))
                else:
                    g.add((pokemon_uri, BULBA[key], Literal(clean_value)))
            else:
                if key.startswith("height"):
                    g.add((pokemon_uri, SCHEMA.height, Literal(strip_html_tags(value))))
                elif key.startswith("weight"):
                    g.add((pokemon_uri, SCHEMA.weight, Literal(strip_html_tags(value))))
                elif key in ["image","name", "jname", "tmname", "ndex", "category", "color", "friendship", "catchrate", "generation", "gender", "gendercode", "body", "lv100exp", "oldexp"]:
                    g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
                elif key.endswith("note"):
                    g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))
                else:
                    g.add((pokemon_uri, URIRef(BULBA[key]), Literal(strip_html_tags(value))))


    return g.serialize(format="turtle").encode('utf-8')

def main():
    with open('data/python-data/infoboxes/pokemon_infoboxes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    rdf_data = json_to_rdf(data)
    with open('data/python-data/rdf/pokemons_linked.ttl', 'wb') as file:
        file.write(rdf_data)

if __name__ == '__main__':
    main()

    
