import json
from rdflib import Graph
from tqdm import tqdm

# JSON-LD context mapping fields to appropriate schema.org IRIs
CONTEXT = {
    "@context": {
        "colorscheme": "http://schema.org/color",
        "name": "http://schema.org/name",
        "jpname": "http://schema.org/alternateName",
        "jptrans": "http://schema.org/alternateName",
        "jptranslit": "http://schema.org/alternateName",
        "text3": "http://schema.org/description",
        "text4": "http://schema.org/description",
        "text5": "http://schema.org/description",
        "text6": "http://schema.org/description",
        "text7": "http://schema.org/description",
        "text8": "http://schema.org/description",
        "gen": "http://schema.org/version",
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
            **data
        }
        # Parse JSON-LD into the RDF graph
        graph.parse(data=json.dumps(data_with_context), format="json-ld")

    # Serialize RDF to Turtle
    return graph.serialize(format="turtle").decode("utf-8")


def main():
    with open('data/python-data/ability_infoboxes.json', 'r') as file:
        data = json.load(file)
        
    with open('data/python-data/rdf/abilities.ttl', 'w', encoding='utf-8') as file:
        file.write(json_to_rdf(data))
        
if __name__ == '__main__':
    main()