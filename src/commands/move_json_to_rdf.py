from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
import json
from rdflib import Graph
from tqdm import tqdm
import urllib.parse
from src.utils.html_handler import *

def json_to_rdf(json_list, base_url="http://localhost:3030/bulba_vocab#"):
    SCHEMA = Namespace("http://schema.org/")
    BULBA = Namespace(base_url)

    g = Graph()
    g.bind("schema", SCHEMA)
    g.bind("bulba", BULBA)

    for data in tqdm(json_list, desc="Converting JSON to RDF"):
        move_name = data.get("name", "Unknown")
        uri_name = move_name.replace(" ", "_") 
        move_uri = URIRef(base_url + urllib.parse.quote(uri_name))

        g.add((move_uri, RDF.type, SCHEMA.Thing))
        g.add((move_uri, RDF.type, URIRef(BULBA.Move)))  

        for key, value in data['infobox'].items():
            if not value:
                continue
            sanitized_key = key.replace('#', '_')
            g.add((move_uri, URIRef(BULBA[sanitized_key]), Literal(strip_html_tags(value))))

    return g.serialize(format="turtle").encode('utf-8')


def main():
    with open('data/python-data/infoboxes/move_infoboxes.json', 'r') as file:
        data = json.load(file)
    
    rdf_data = json_to_rdf(data)
    print(rdf_data)
    with open('data/python-data/rdf/moves.ttl', 'wb') as file:
        file.write(rdf_data)
        
if __name__ == '__main__':
    main()