import rdflib
from rdflib import RDF

def check_duplicates_in_vocab(vocab_file):
    graph = rdflib.Graph()
    graph.parse(vocab_file, format='turtle')
    
    property_counts = {}
    
    for s in graph.subjects(RDF.type, RDF.Property):
        property_counts[s] = property_counts.get(s, 0) + 1
    
    duplicates = [str(prop) for prop, count in property_counts.items() if count > 1]
    
    return duplicates

if __name__ == "__main__":
    vocab_ttl_path = "data/python-data/rdf/bulba_vocab.ttl"
    dup_props = check_duplicates_in_vocab(vocab_ttl_path)

    if dup_props:
        print("Found duplicate property declarations:")
        for prop_uri in dup_props:
            print(f"  - {prop_uri}")
    else:
        print("No duplicate property declarations found.")
