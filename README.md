
# Contributors

- Mounir ROUIBI  
- Mathieu SROUR  

# Overview

- This project uses **Python 3.11** and **Docker** to run a Fuseki triplestore.
- The instructions assume we are using a **Linux-based** system.
- All the relevant code is in the **src** folder.
- All the relevant data will be in the **data/python-data** folder.
- The **playground** folder was created to explore and test functionalities of the **rdflib** library for learning purposes.

# How to Use

1. **Navigate to the Project's Root Directory**  

2. **Install Dependencies**  
    You can either create a virtual Python environment or skip this step and install the dependencies directly:
    - To create a virtual environment (optional):

        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

    - Install the required Python packages:

        ```bash
        pip install -r requirements.txt
        ```

3. **Set the Python Path**  
    Export the project directory as the Python path:

    ```bash
    export PYTHONPATH=$(pwd)
    ```

4. **Start the Fuseki Triplestore**  
    Make sure you have Docker installed on your environment and run one of the following commands:

    ```bash
    docker compose up --build
    ```

    Or

    ```bash
    docker-compose up --build
    ```

5. **Dataset Creation**  
    In the Fuseki triplestore, create two datasets:

   - The first one is named **bulba_vocab** and uses the file **data/python-data/rdf/bulba_vocab.ttl** to host the vocabulary.
   - The second one is named **dataset** and uses the files **data/python-data/rdf/pokemons_linked.ttl**, **data/python-data/rdf/moves.ttl**, and **data/python-data/rdf/abilities.ttl**.

6. **Run the Visual Interface**  
    Simply run:

    ```bash
    python src/main.py
    ```

    from the root directory. Then access it through this [link](http://127.0.0.1:5000).  
    For a given entity stored in the triplestore, here is an example [link](http://127.0.0.1:5000/Pikachu_%28Pok%C3%A9mon%29).

# Process of Creating an RDF File

In order to retrieve data from Bulbapedia, we created a JSON file containing every page in the wiki called **pages_list.json**, which will be used in the steps below.

We create three files for three types of infoboxes:

## Pokémon Infobox

1. We obtain a list of potential Pokémon pages by creating a file **pokemon_pages_list.json** from **pages_list.json**. This is done by selecting all pages that have the word "Pokémon" in their title. (See **src/commands/get_pokemons_pages_list.py**)

2. After creating a list of potential Pokémon pages, we go through the wikitext of each page and look for the "Pokémon Infobox". If we succeed in finding it, then the page is confirmed to be a Pokémon page and we get the infobox as json data and store it in the **data/python-data/infobox/pokemons.ttl**. This is done in the file **src/commands/get_pokemons_infoboxes.py**.

3. We transform the infobox, which is in JSON format, into RDF in the file **src/commands/pokemon_json_to_rdf.py**, given that we created the abilities rdf before this point.

4. Finally, we add the different languages given in **pokedex-i18n.tsv** to the triples in **pokemon.ttl**. This is done in the file **src/commands/add_languages_to_pokemons.py**. We also add links to the web pages, by running **src/commands/add links to identities.py**.

## The Rest of the RDF Files

We follow the exact same steps for the **move infoboxes** and the **abilities infoboxes**, using the same naming convention for the files in the **src/commands** folder.

## SHACL Classes

In order to validate our rdfs against SHACL, we need to create SHACL nodes. This is done in **src/commands/create_shacl_classes.py**. After running this file, the validation can be done by running **src/commands/validate_rdf_against_shacl.py**.
