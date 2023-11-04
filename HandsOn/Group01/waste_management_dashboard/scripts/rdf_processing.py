# Script for RDF data processing
import requests
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Define the SPARQL query
sparql_query = """
SELECT ?population
WHERE {
  wd:Q2017682 wdt:P1082 ?population.
}
"""

# Define the Wikidata SPARQL endpoint URL
wikidata_sparql_endpoint = "https://query.wikidata.org/sparql"

# Send the SPARQL query to Wikidata
response = requests.post(
    wikidata_sparql_endpoint,
    data={"query": sparql_query},
    headers={"Accept": "application/sparql-results+json"},
)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()

    # Extract and display the population value
    for binding in results["results"]["bindings"]:
        population = binding["population"]["value"]
        print(f"Population of Moncloa district of Madrid: {population}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


from rdflib import Graph, Namespace

# Initialize a graph
g = Graph()

# Parse in an RDF file hosted at the specified location (placeholder here)
g.parse("data/rdf-with-links.ttl", format="turtle")

# Define the namespaces based on your PREFIXES
TI = Namespace("http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
BASE = Namespace("http://madridwastemanagement.org/")
NSO = Namespace("http://madridwastemanagement.org/group01/ontology/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
DBO = Namespace("https://dbpedia.org/ontology/")
GEOCOD = Namespace("https://www.gleif.org/ontology/Geocoding/")
GEOF = Namespace("http://www.mindswap.org/2003/owl/geo/geoFeatures20040307.owl#")
TIME = Namespace("http://www.w3.org/2006/time#")
WST = Namespace("http://www.disit.org/km4city/schema#")

# Bind the namespaces
g.bind("ti", TI)
g.bind("dc", DC)
g.bind("base", BASE)
g.bind("nso", NSO)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("dbo", DBO)
g.bind("geocod", GEOCOD)
g.bind("geof", GEOF)
g.bind("time", TIME)
g.bind("wst", WST)

# Write the query
query = """
SELECT DISTINCT ?districtName
WHERE {
  ?districtInstance a dbo:District ;
                    dbo:districtName ?districtName .
}
"""

# Execute the query
for row in g.query(query):
    print(f"District Name: {row.districtName}")
