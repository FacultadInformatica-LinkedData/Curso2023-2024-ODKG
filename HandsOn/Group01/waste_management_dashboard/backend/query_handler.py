
import requests

def execute_query(wikidata_id):
    query = f"""
    SELECT ?population ?image ?coordinateLocation
    WHERE {{
      wd:{wikidata_id} wdt:P1082 ?population.
      wd:{wikidata_id} wdt:P18 ?image.
      wd:{wikidata_id} wdt:P625 ?coordinateLocation.
    }}
    """

    # Send the query to the Wikidata SPARQL endpoint and retrieve the results
    endpoint_url = 'https://query.wikidata.org/sparql'
    response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})
    
    if response.status_code == 200:
        population_data = response.json()
        return population_data
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
