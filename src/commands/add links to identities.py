from rdflib import Graph, Namespace, URIRef
import urllib.parse

# Define namespaces
BULBA = Namespace("http://localhost:3030/bulba_vocab#")
PAGE = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
SCHEMA = Namespace("http://schema.org/")

# Load the existing Pokémon RDF graph
pokemon_graph = Graph()
pokemon_graph.parse("data/python-data/rdf/pokemons_linked.ttl", format="turtle")

# Add schema:mainEntityOfPage relationships
for subject in pokemon_graph.subjects():
    if str(subject).startswith(str(BULBA)):
        # Extract the Pokémon name from the URI and decode it to avoid double encoding
        pokemon_name = urllib.parse.unquote(str(subject).split("#")[-1])
        # Encode properly for the page URI
        page_uri = URIRef(PAGE + urllib.parse.quote(pokemon_name))
        # Add the schema:mainEntityOfPage triple
        pokemon_graph.add((subject, SCHEMA.mainEntityOfPage, page_uri))

# Save the updated RDF graph
pokemon_graph.serialize(destination="data/python-data/rdf/pokemons_linked.ttl", format="turtle")
print("Added schema:mainEntityOfPage links to the Pokémon RDF graph without double encoding.")

abilities_graph = Graph()
abilities_graph.parse("data/python-data/rdf/abilities.ttl", format="turtle")

for subject in abilities_graph.subjects():
    if str(subject).startswith(str(BULBA)):
        # Extract the Pokémon name from the URI and decode it to avoid double encoding
        ability_name = urllib.parse.unquote(str(subject).split("#")[-1])
        # Encode properly for the page URI
        page_uri = URIRef(PAGE + urllib.parse.quote(ability_name))
        # Add the schema:mainEntityOfPage triple
        abilities_graph.add((subject, SCHEMA.mainEntityOfPage, page_uri))

abilities_graph.serialize(destination="data/python-data/rdf/abilities.ttl", format="turtle")
print("Added schema:mainEntityOfPage links to the Pokémon RDF graph without double encoding.")