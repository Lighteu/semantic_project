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

# Validate Pokémon's body
shacl_graph.add((pokemon_shape, SH.property, BULBA.body))
shacl_graph.add((BULBA.body, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.body, SH.pattern, Literal("^\\d{2}$")))  # 2 digit number

# Validate Pokémon's Primary Type (type1 is required)
shacl_graph.add((pokemon_shape, SH.property, BULBA.type1))
shacl_graph.add((BULBA.type1, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.type1, SH.minCount, Literal(1)))
shacl_graph.add((BULBA.type1, SH.maxCount, Literal(1)))

# Validate Pokémon's Secondary Type (type2 is optional)
shacl_graph.add((pokemon_shape, SH.property, BULBA.type2))
shacl_graph.add((BULBA.type2, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.type2, SH.maxCount, Literal(1)))

for ability_property in [BULBA.ability1, BULBA.ability2, BULBA.abilityd]:
    shacl_graph.add((pokemon_shape, SH.property, ability_property))
    shacl_graph.add((ability_property, SH.class_, BULBA.Ability))

# Validate Pokémon's Height and Weight
for measure_property in [SCHEMA.height, SCHEMA.weight]:
    shacl_graph.add((pokemon_shape, SH.property, measure_property))
    shacl_graph.add((measure_property, SH.datatype, SCHEMA.Text))
    shacl_graph.add((measure_property, SH.minCount, Literal(1)))
    shacl_graph.add((measure_property, SH.maxCount, Literal(1)))

# Validate Pokémon's Category
shacl_graph.add((pokemon_shape, SH.property, BULBA.category))
shacl_graph.add((BULBA.category, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.category, SH.minCount, Literal(1)))
shacl_graph.add((BULBA.category, SH.maxCount, Literal(1)))

# Validate Pokémon's Color
shacl_graph.add((pokemon_shape, SH.property, BULBA.color))
shacl_graph.add((BULBA.color, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.color, SH.minCount, Literal(1)))
shacl_graph.add((BULBA.color, SH.maxCount, Literal(1)))

# Validate Pokémon's Generation
shacl_graph.add((pokemon_shape, SH.property, BULBA.generation))
shacl_graph.add((BULBA.generation, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.generation, SH.minCount, Literal(1)))
shacl_graph.add((BULBA.generation, SH.maxCount, Literal(1)))
shacl_graph.add((BULBA.generation, SH.pattern, Literal("^\\d+$")))  # Only digits allowed


# Ensure Pokémon has schema:mainEntityOfPage
shacl_graph.add((pokemon_shape, SH.property, SCHEMA.mainEntityOfPage))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.nodeKind, SH.IRI))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.minCount, Literal(1)))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.maxCount, Literal(1)))

# Validate Pokémon's catchrate
shacl_graph.add((pokemon_shape, SH.property, BULBA.catchrate))
shacl_graph.add((BULBA.catchrate, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.catchrate, SH.pattern, Literal("^\\d+$")))  # Only digits allowed


# Validate Pokémon's gendercode
shacl_graph.add((pokemon_shape, SH.property, BULBA.gendercode))
shacl_graph.add((BULBA.gendercode, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.gendercode, SH.pattern, Literal("^\\d+$")))  # Only digits allowed

# Validate Pokémon's Egg Cycles (numeric string)
shacl_graph.add((pokemon_shape, SH.property, BULBA.eggcycles))
shacl_graph.add((BULBA.eggcycles, SH.datatype, SCHEMA.Text))
shacl_graph.add((BULBA.eggcycles, SH.pattern, Literal("^\\d+$")))  # Only digits allowed





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

# Validate Ability colorscheme
shacl_graph.add((ability_shape, SH.property, BULBA.colorscheme))
shacl_graph.add((BULBA.colorscheme, SH.datatype, SCHEMA.Text))

# Add schema:mainEntityOfPage for Abilities
shacl_graph.add((ability_shape, SH.property, SCHEMA.mainEntityOfPage))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.nodeKind, SH.IRI))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.minCount, Literal(1)))
shacl_graph.add((SCHEMA.mainEntityOfPage, SH.maxCount, Literal(1)))


# Serialize the SHACL shapes to a Turtle file
shacl_graph.serialize(destination="data/python-data/rdf/shacl_shapes.ttl", format="turtle")
print("Detailed SHACL shapes have been generated and saved to 'shacl_shapes.ttl'.")