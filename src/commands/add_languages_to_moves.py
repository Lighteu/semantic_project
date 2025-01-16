from rdflib import Graph, Namespace, Literal, RDF
import csv

# Map language names to ISO 639-1 codes
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
}

def update_rdf_with_languages(rdf_file, tsv_file, output_file):
    # Load RDF data
    g = Graph()
    g.parse(rdf_file, format="turtle")
    
    # Dynamically extract namespaces
    namespace_dict = {prefix: namespace for prefix, namespace in g.namespaces()}
    if "bulba" not in namespace_dict:
        raise ValueError("Namespace 'bulba' not found in the RDF file.")
    BULBA = Namespace(namespace_dict["bulba"])
    
    # Load TSV data
    language_data = {}
    with open(tsv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t", fieldnames=["type", "id", "label", "language"])
        for row in reader:
            if row["type"] != "move":
                continue
            move_id = row["id"]
            language = row["language"]
            name = row["label"]
            if move_id not in language_data:
                language_data[move_id] = []
            language_data[move_id].append((language, name))
    
    # Update RDF triples
    for move in g.subjects(RDF.type, BULBA["Move"]):
        english_name = g.value(move, BULBA["name"])
        if english_name:
            for move_id, translations in language_data.items():
                for lang, name in translations:
                    if lang == "English" and name == str(english_name):
                        # Add language-specific names to RDF with proper language tags
                        for lang_name, localized_name in translations:
                            lang_code = LANGUAGE_CODES.get(lang_name, lang_name.lower())
                            g.add((move, BULBA["name"], Literal(localized_name, lang=lang_code)))

    # Save updated RDF to file
    g.serialize(destination=output_file, format="turtle")
    
if __name__ == '__main__':
    rdf_file = "data/python-data/rdf/moves.ttl"
    tsv_file = "data/python-data/pokedex-i18n.tsv"
    output_file = "data/python-data/rdf/moves.ttl"

    update_rdf_with_languages(rdf_file, tsv_file, output_file)
