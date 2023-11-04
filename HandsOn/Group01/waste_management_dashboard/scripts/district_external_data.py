# Script for retrieving external information for each district
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/district_population')
def district_population():
    wikidata_id = request.args.get('wikidataId')
    query = f"""
    SELECT ?population ?image ?coordinateLocation
    WHERE {{
      wd:{wikidata_id} wdt:P1082 ?population.
      wd:{wikidata_id} wdt:P18 ?image.
      wd:{wikidata_id} wdt:P625 ?coordinateLocation.
    }}
    """

    # Here you would send the query to the SPARQL endpoint and retrieve the results
    # For example (endpoint URL needs to be the actual Wikidata query service URL):
    # response = requests.get('https://query.wikidata.org/sparql', params={'query': query, 'format': 'json'})
    # population_data = response.json()

    # For now, let's just return the query for demonstration purposes
    return query

if __name__ == '__main__':
    app.run(debug=True)
