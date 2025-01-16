from pyshacl import validate

# Paths to RDF data and SHACL shape files
rdf_data_path = "data/python-data/rdf/pokemons_linked.ttl"
shacl_shape_path = "data/python-data/rdf/shacl_shapes.ttl"

# Run SHACL validation
def validate_kg():
    conforms, results_graph, results_text = validate(
        data_graph=rdf_data_path,
        shacl_graph=shacl_shape_path,
        inference='rdfs',
        abort_on_first=False,
        meta_shacl=False,
        debug=False
    )

    if conforms:
        print("Knowledge Graph conforms to the SHACL schema.")
    else:
        print("Validation errors detected:")
        print(results_text.encode('utf-8'))

if __name__ == "__main__":
    validate_kg()
