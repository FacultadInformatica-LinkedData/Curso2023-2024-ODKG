import rdflib, requests
from flask import Flask, render_template, request

#######################################################################################################################################################
#######################################################################################################################################################
########################################################## Environment ###############################################33###########################
#######################################################################################################################################################


app = Flask(__name__)

# Local database
g = rdflib.Graph()
g.parse("data/rdf-with-links.ttl", format="ttl")


#######################################################################################################################################################
#######################################################################################################################################################
########################################################## SPARQL Queries ###############################################33###########################
#######################################################################################################################################################
def run_district_details_query(district_id):
    endpoint_url = "https://query.wikidata.org/sparql"
    """
           Given a district id it retrieves the details of the district from wikidata
           :param district_name:
           :return:
           """
    query = f"""
            PREFIX schema: <http://schema.org/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX wd: <http://www.wikidata.org/entity/>


            SELECT ?population ?description ?area ?coordinates ?label
            WHERE {{
              BIND(wd:{district_id} AS ?district)
              ?district wdt:P1082 ?population.
              ?district wdt:P2046 ?area.
              ?district schema:description ?description.
              ?district wdt:P625 ?coordinates.
              ?district rdfs:label ?label . 
              FILTER (langMatches( lang(?label), "ES" ) )  
              FILTER(LANG(?description) = "en")
            }}
            """
    try:
        response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})
        data = response.json()
        results = data['results']['bindings']
        output = []
        for result in results:
            output_dict = {
                'population': result['population']['value'],
                'description': result['description']['value'],
                'area': result['area']['value'],
                'coordinates': result['coordinates']['value'],
                'name': result['label']['value']
            }
            output.append(output_dict)
            return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def run_sparql_query(district_name):
    """
    Given an dsitrict name it generates th waste amount for each type of waste for each month
    :param district_name:
    :return:
    """
    g = rdflib.Graph()
    g.parse(
        "data/rdf-with-links.ttl",
        format="ttl",
    )

    query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX nso: <http://madridwastemanagement.org/group01/ontology/>
            PREFIX wst: <http://www.disit.org/km4city/schema#>
            PREFIX time: <http://www.w3.org/2006/time#>

            SELECT ?wasteName ?wikidataLink ?m (SUM(?val) AS ?totalAmount)
            WHERE {{
              ?districtInstance a dbo:District ;
                                rdfs:label "{district_name}";
                                wst:hasResidue ?wasteinstance.
              ?wasteinstance rdfs:label ?wasteName;
                             owl:sameAs ?wikidataLink;
                             nso:hasTotal ?totalinstance.
              ?totalinstance nso:value ?val;
                             time:month ?m.
            }}
            GROUP BY ?wasteName ?wikidataLink ?m
            ORDER BY ?m ?wasteName
            """
    results = g.query(query)
    output = []
    for row in results:
        output_dict = {
            "wasteName": str(row[0]),
            "wikidataLink": str(row[1]),
            "month": str(row[2]),
            "totalAmount": str(row[3]),
        }
        output.append(output_dict)
    return output
def run_wasteType_query(wikidata_id):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = f"""
            PREFIX schema: <http://schema.org/>
            SELECT ?description
            WHERE {{
              wd:{wikidata_id} schema:description ?description.
              FILTER(LANG(?description) = "en")
            }}
            LIMIT 1
            """
    try:
        response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})
        data = response.json()
        results = data['results']['bindings']
        if results:
            output = results[0]['description']['value']
            return output
        else:
            return "No description found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while fetching the description"

#######################################################################################################################################################
#######################################################################################################################################################
########################################################## Rooter ######### ###############################################33###########################
#######################################################################################################################################################


### If we end up with to many routes all the functions will be placed in separted folder called router or controler (MVC pattern)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/district")
def district():
    district_name = request.args.get("name")
    district_id = request.args.get("wikidataID")
    waste_results = run_sparql_query(district_name)
    district_details = run_district_details_query(district_id)
    return render_template("district.html", waste_results=waste_results, district_details=district_details)

@app.route("/wasteType")
def waste_type():
    wikidata_id = request.args.get("wikidata_id")
    result = run_wasteType_query(wikidata_id)
    return render_template("wasteType.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
