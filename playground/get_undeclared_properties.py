import rdflib
from rdflib.namespace import RDF
def find_undeclared_properties(data_ttl_files, vocab_ttl_file):
    vocab_graph = rdflib.Graph()
    vocab_graph.parse(vocab_ttl_file, format='turtle')
    
    declared_properties = set()
    for subj in vocab_graph.subjects(RDF.type, RDF.Property):
        declared_properties.add(subj)

    used_properties = set()
    for ttl_file in data_ttl_files:
        data_graph = rdflib.Graph()
        data_graph.parse(ttl_file, format='turtle')
        
        for s, p, o in data_graph:
            used_properties.add(p)

    undeclared = used_properties - declared_properties

    return undeclared

if __name__ == "__main__":
    data_files = ["data/python-data/rdf/abilities.ttl", "data/python-data/rdf/pokemons.ttl", "data/python-data/rdf/moves.ttl"]  
    vocab = "data/python-data/rdf/bulba_vocab.ttl"           
    properties_used = find_undeclared_properties(data_files, vocab)
    
    print("Properties used that are declared in the vocabulary:")
    for prop in properties_used:
        print( prop)
