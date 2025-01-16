from flask import Flask, request, render_template, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
import os 

app = Flask(__name__, template_folder=f"{os.getcwd()}/src/templates")

# Fuseki SPARQL endpoint URL
SPARQL_ENDPOINT = "http://localhost:3030/dataset/sparql"

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

    
if __name__ == "__main__":
    app.run(debug=True)
