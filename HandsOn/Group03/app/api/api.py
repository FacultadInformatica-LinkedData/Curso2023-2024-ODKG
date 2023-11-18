from flask import Flask, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS
from qwikidata.sparql  import return_sparql_query_results
import json 


app = Flask(__name__)
CORS(app)

# URL de SPARQL endpoint de Jena
SPARQL_ENDPOINT_ACTIVITIES = "http://localhost:3030/activities"
SPARQL_ENDPOINT_PARK = "http://localhost:3030/parks"

@app.route('/query-activities', methods=['GET'])
def sparql_query():
    district = request.args.get('district')
    neighborhood = request.args.get('neighborhood')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    
    query = """
        
        PREFIX ns1: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?id ?title ?description ?locationName ?locationUrl ?locationAccessibility ?startDate ?endDate ?contentURL ?addressName ?neighborhoodName ?districtName ?wikidataUrlDistrict
        WHERE {
        ?activity a <http://vidaactivamadrid.es/info/ontology/class#Activity> ;
            ns1:name ?title ;
            ns1:id ?id;
            ns1:description ?description ;
            ns1:takesPlaceIn ?location ;
            ns1:startDate ?startDate ;
            ns1:endDate ?endDate ;
            ns1:contentURL ?contentURL .
        ?location ns1:name ?locationName ;
            ns1:facilityURL ?locationUrl ;
            ns1:accessibility ?locationAccessibility;
            ns1:hasAddress ?address .
        ?address ns1:name ?addressName;
            ns1:isInNeighborhood ?neighborhood .
        ?neighborhood ns1:name ?neighborhoodName ;
            ns1:isInDistrict ?district .
        ?district ns1:name ?districtName ;
                    owl:sameAs ?wikidataUrlDistrict .

    """

    if district and district != "null":
        query += f""" FILTER (?districtName = "{district}") . """
    if neighborhood and neighborhood != "null":
        query += f""" FILTER (?neighborhoodName = "{neighborhood}") ."""
    if startDate and startDate != "null":
        query += f""" FILTER (?startDate >= "{startDate}"^^xsd:dateTime) ."""
    if endDate and endDate != "null":
        query += f""" FILTER (?startDate <= "{endDate}"^^xsd:dateTime) ."""
 
    query += """ } """

    # print(query)
    # Inicializando SPARQLWrapper
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_ACTIVITIES)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/query-parks', methods=['GET'])
def sparql_query_park():
    district = request.args.get('district')
    neighborhood = request.args.get('neighborhood')

    query = """
        PREFIX ns1: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sq: <https://schema.org/>

        SELECT DISTINCT ?id_park ?title ?neighboardhood_name ?district_name ?wikidataUrlDistrict
        WHERE {
        ?s a <http://vidaactivamadrid.es/info/ontology/class#Park> .
        ?s sq:name ?title .
        ?s ns1:id_park ?id_park .
        ?s ns1:isInNeighborhood ?uriNeighboardhood .
        ?uriNeighboardhood ns1:name ?neighboardhood_name .
        ?uriNeighboardhood ns1:isInDistrict ?uriDistric .
        ?uriDistric ns1:name ?district_name ;
            owl:sameAs ?wikidataUrlDistrict .
        
    """

    if district and district != "null":
        query += f""" FILTER (?district_name = "{district}") . """
    if neighborhood and neighborhood != "null":
        query += f""" FILTER (?neighboardhood_name = "{neighborhood}") ."""
 
    query += """ } """
    # Inicializando SPARQLWrapper
    
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_PARK)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/query-park-district', methods=['GET'])
def sparql_query_park_district():

    query = """
        PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?nameDistrict
        WHERE {
        ?s a <http://vidaactivamadrid.es/info/ontology/class#District> ;
            nsp:name ?nameDistrict ;
    """

    query += """ } ORDER BY ?nameDistrict"""
    # Inicializando SPARQLWrapper
    
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_PARK)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/query-park-neighborhood', methods=['GET'])
def sparql_query_park_neighborhood():
    district = request.args.get('district')

    query = """
        PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        SELECT ?nameDistrict ?nameNeighborhood
        WHERE {
            ?subDistrict a <http://vidaactivamadrid.es/info/ontology/class#District> ;
                nsp:name ?nameDistrict .
            ?subNeighborhood a <http://vidaactivamadrid.es/info/ontology/class#Neighborhood> ;
                nsp:name ?nameNeighborhood ;
                nsp:isInDistrict ?subDistrict .  # Asociación del barrio con el distrito
    """

    query += f""" FILTER (?nameDistrict = "{district}") . """
    query += """ } """
    # Inicializando SPARQLWrapper
    
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_PARK)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)



@app.route('/query-activities-district', methods=['GET'])
def sparql_query_activities_district():

    query = """
        PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?nameDistrict
        WHERE {
        ?s a <http://vidaactivamadrid.es/info/ontology/class#District> ;
            nsp:name ?nameDistrict ;
    """

    query += """ } ORDER BY ?nameDistrict"""
    # Inicializando SPARQLWrapper
    
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_ACTIVITIES)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/query-activities-neighborhood', methods=['GET'])
def sparql_query_activities_neighborhood():
    district = request.args.get('district')

    query = """
        PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?nameDistrict ?nameNeighborhood
        WHERE {
            ?subDistrict a <http://vidaactivamadrid.es/info/ontology/class#District> ;
                nsp:name ?nameDistrict .
            ?subNeighborhood a <http://vidaactivamadrid.es/info/ontology/class#Neighborhood>;
                nsp:name ?nameNeighborhood ;
                nsp:isInDistrict ?subDistrict .
    """

    query += f""" FILTER (?nameDistrict = "{district}") . """
    query += """ } """
    # Inicializando SPARQLWrapper
    
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_ACTIVITIES)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Obteniendo resultados y convirtiendo en JSON
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/query-district-wikidata', methods=['GET'])
def sparql_query_district_wikidata():
    # wikidata = request.args.get('wikidata')
    wikidata = "Q953368"
    query_string = """
        SELECT ?population ?locationImage ?area ?coordinate_location
        WHERE {
            OPTIONAL { wd:Q656196 wdt:P2046 ?area. }
            OPTIONAL { wd:Q656196 wdt:P17 ?country. }
            OPTIONAL { wd:Q656196 wdt:P625 ?coordinate_location. }
    """

    query_string += f" wd:{wikidata} wdt:P1082 ?population . "
    query_string += f" wd:{wikidata} wdt:P18 ?locationImage . "
    query_string += """ } """

    results = return_sparql_query_results(query_string)

    bindings = results["results"]["bindings"]
    result = [{k: v["value"] for k, v in item.items()} for item in bindings]

    return jsonify(result)


@app.route('/')
def hello():
    return 'Backend de Vida Activa Madrid'

if __name__ == "__main__":
    app.run(port=8080)



""" DISTRICT
activities
PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?nameDistrict ?linkWikidata
WHERE {
  ?s a <http://vidaactivamadrid.es/info/ontology/class#Neighborhood2>;
     nsp:name ?nameDistrict ;
  	 owl:sameAs ?linkWikidata
}


PREFIX nsp: <http://vidaactivamadrid.es/info/ontology/property#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

parks
SELECT DISTINCT ?nameDistrict
WHERE {
  ?s a <http://vidaactivamadrid.es/info/ontology/class#District> ;
     nsp:name ?nameDistrict ;
     owl:sameAs ?linkWikidata .
}

"""