from rdflib import Graph, Namespace, RDF, Literal

# Define namespaces
BULBA = Namespace("http://localhost:3030/bulba_vocab#")
SCHEMA = Namespace("http://schema.org/")
SH = Namespace("http://www.w3.org/ns/shacl#")

pokemon_graph = Graph()
pokemon_graph.parse("data/python-data/rdf/pokemons_linked.ttl", format="turtle")

ability_graph = Graph()
ability_graph.parse("data/python-data/rdf/abilities.ttl", format="turtle")

# Create a new graph for SHACL shapes
shacl_graph = Graph()
shacl_graph.bind("sh", SH)
shacl_graph.bind("bulba", BULBA)
shacl_graph.bind("schema", SCHEMA)

pokemon_shape = BULBA.PokemonShape
shacl_graph.add((pokemon_shape, RDF.type, SH.NodeShape))
shacl_graph.add((pokemon_shape, SH.targetClass, BULBA.Pokemon))

# Validate Pokémon's National Dex Number
shacl_graph.add((pokemon_shape, SH.property, BULBA.ndex))
shacl_graph.add((BULBA.ndex, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.ndex, SH.pattern, Literal("^\\d{3,4}$")))  # 3 or 4 digit number

# Validate Pokémon's Primary Type (type1 is required)
shacl_graph.add((pokemon_shape, SH.property, BULBA.type1))
shacl_graph.add((BULBA.type1, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.type1, SH.minCount, Literal(1)))

for ability_property in [BULBA.ability1, BULBA.ability2, BULBA.abilityd]:
    shacl_graph.add((pokemon_shape, SH.property, ability_property))
    shacl_graph.add((ability_property, SH.class_, BULBA.Ability))

# Validate Pokémon's Height and Weight
for measure_property in [SCHEMA.height, SCHEMA.weight]:
    shacl_graph.add((pokemon_shape, SH.property, measure_property))
    shacl_graph.add((measure_property, SH.datatype, SCHEMA.Text))
    shacl_graph.add((measure_property, SH.minCount, Literal(1)))




# Define SHACL Shape for Abilities
ability_shape = BULBA.AbilityShape
shacl_graph.add((ability_shape, RDF.type, SH.NodeShape))
shacl_graph.add((ability_shape, SH.targetClass, BULBA.Ability))

# Validate Ability name
shacl_graph.add((ability_shape, SH.property, BULBA.name))
shacl_graph.add((BULBA.name, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.name, SH.minCount, Literal(1)))

# Validate Ability generation
shacl_graph.add((ability_shape, SH.property, BULBA.gen))
shacl_graph.add((BULBA.gen, SH.datatype, SCHEMA.Text))

# Serialize the SHACL shapes to a Turtle file
shacl_graph.serialize(destination="data/python-data/rdf/shacl_shapes.ttl", format="turtle")
print("Detailed SHACL shapes have been generated and saved to 'shacl_shapes.ttl'.")