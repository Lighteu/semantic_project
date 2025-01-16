from rdflib import Graph, Namespace, RDF, Literal, BNode

# Define namespaces
BULBA = Namespace("http://localhost:3030/bulba_vocab#")
SCHEMA = Namespace("http://schema.org/")
SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")


# Load the RDF data (pokemons.ttl and abilities.ttl)
pokemon_graph = Graph()
pokemon_graph.parse("data/python-data/rdf/pokemons_linked.ttl", format="turtle")

ability_graph = Graph()
ability_graph.parse("data/python-data/rdf/abilities.ttl", format="turtle")

# Create a new graph for SHACL shapes
shacl_graph = Graph()
shacl_graph.bind("sh", SH)
shacl_graph.bind("bulba", BULBA)
shacl_graph.bind("schema", SCHEMA)
shacl_graph.bind("xsd", XSD)

# Define SHACL Shape for Pokémon
pokemon_shape = BULBA.PokemonShape
shacl_graph.add((pokemon_shape, RDF.type, SH.NodeShape))
shacl_graph.add((pokemon_shape, SH.targetClass, BULBA.Pokemon))

# Validate Pokémon's National Dex Number
ndex_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, ndex_shape))
shacl_graph.add((ndex_shape, SH.path, BULBA.ndex))
shacl_graph.add((ndex_shape, SH.datatype, XSD.string))
shacl_graph.add((ndex_shape, SH.pattern, Literal(r"^\d{3,4}$")))

shacl_graph.add((ndex_shape, SH.minCount, Literal(1)))

# Validate Pokémon's Body (2-digit number)
body_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, body_shape))
shacl_graph.add((body_shape, SH.path, BULBA.body))
shacl_graph.add((body_shape, SH.datatype, XSD.string))
shacl_graph.add((body_shape, SH.pattern, Literal(r"^\d{2}$")))

# Validate Pokémon's Primary Type (type1 is required)
type1_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, type1_shape))
shacl_graph.add((type1_shape, SH.path, BULBA.type1))
shacl_graph.add((type1_shape, SH.datatype, XSD.string))
shacl_graph.add((type1_shape, SH.minCount, Literal(1)))

# Validate Pokémon's Secondary Type (type2 is optional)
type2_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, type2_shape))
shacl_graph.add((type2_shape, SH.path, BULBA.type2))
shacl_graph.add((type2_shape, SH.datatype, XSD.string))
shacl_graph.add((type2_shape, SH.maxCount, Literal(1)))

# Validate Pokémon's Abilities
for ability_property in [BULBA.ability1, BULBA.ability2, BULBA.abilityd]:
    ability_shape = BNode()
    shacl_graph.add((pokemon_shape, SH.property, ability_shape))
    shacl_graph.add((ability_shape, SH.path, ability_property))
    shacl_graph.add((ability_shape, SH.class_, BULBA.Ability))

# Validate Pokémon's Height and Weight
for measure_property in [SCHEMA.height, SCHEMA.weight]:
    measure_shape = BNode()
    shacl_graph.add((pokemon_shape, SH.property, measure_shape))
    shacl_graph.add((measure_shape, SH.path, measure_property))
    shacl_graph.add((measure_shape, SH.datatype, XSD.string))
    shacl_graph.add((measure_shape, SH.minCount, Literal(1)))

# Validate Pokémon's Category
category_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, category_shape))
shacl_graph.add((category_shape, SH.path, BULBA.category))
shacl_graph.add((category_shape, SH.datatype, XSD.string))
shacl_graph.add((category_shape, SH.minCount, Literal(1)))

# Validate Pokémon's Color
color_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, color_shape))
shacl_graph.add((color_shape, SH.path, BULBA.color))
shacl_graph.add((color_shape, SH.datatype, XSD.string))
shacl_graph.add((color_shape, SH.minCount, Literal(1)))

# Validate Pokémon's Generation
gen_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, gen_shape))
shacl_graph.add((gen_shape, SH.path, BULBA.generation))
shacl_graph.add((gen_shape, SH.datatype, XSD.string))
shacl_graph.add((gen_shape, SH.minCount, Literal(1)))
shacl_graph.add((gen_shape, SH.pattern, Literal(r"^\d+$")))


# Ensure Pokémon has schema:mainEntityOfPage
main_entity_shape = BNode()
shacl_graph.add((pokemon_shape, SH.property, main_entity_shape))
shacl_graph.add((main_entity_shape, SH.path, SCHEMA.mainEntityOfPage))
shacl_graph.add((main_entity_shape, SH.nodeKind, SH.IRI))
shacl_graph.add((main_entity_shape, SH.minCount, Literal(1)))

# Serialize the SHACL shapes to a Turtle file
shacl_graph.serialize(destination="data/python-data/rdf/shacl_shapes.ttl", format="turtle")
print("SHACL shapes have been generated and saved to 'shacl_shapes.ttl'.")
