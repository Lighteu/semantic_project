from flask import Flask, request, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import os
from src.config import SPARQL_ENDPOINT
from urllib.parse import unquote

app = Flask(__name__, template_folder=f"{os.getcwd()}/src/templates")


def query_fuseki(sparql_query):
    """Query the Fuseki triple store and return results."""
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sparql_query = request.form.get("sparql_query")
        try:
            results = query_fuseki(sparql_query)
            return render_template("index.html", query=sparql_query, results=results)
        except Exception as e:
            return render_template("index.html", query=sparql_query, error=str(e))
    return render_template("index.html")


@app.route("/<path:resource_name>")
def resource_page(resource_name):
    # Handle any needed character replacements or URL-encodings
    resource_name_corrected = (
        resource_name
        .replace("é", "%C3%A9")
        .replace('(', '%28')
        .replace(')', '%29')
    )

    # Construct the full IRI
    full_iri = f"http://localhost:3030/bulba_vocab#{resource_name_corrected}"

    # Build the SPARQL query dynamically
    sparql_query = f"""
    SELECT ?p ?o
    WHERE {{
      <{full_iri}> ?p ?o .
    }}
    """
    print("SPARQL query:", sparql_query)  # For debugging

    try:
        # Execute the query against your Fuseki endpoint
        results = query_fuseki(sparql_query)
        return render_template(
            "resource.html",
            resource_uri=full_iri,
            resource_name=resource_name,  # <-- Pass the raw resource name here
            results=results
        )
    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
