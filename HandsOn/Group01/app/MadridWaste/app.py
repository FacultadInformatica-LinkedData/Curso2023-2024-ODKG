
import rdflib, requests
from flask import Flask, render_template, request, jsonify

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
def run_sparql_query(district_name, year="2021"):
    g = rdflib.Graph()
    g.parse("data/rdf-with-links.ttl", format="ttl")

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
                 nso:hasTotal ?totalinstance.
              ?totalinstance nso:value ?val;
                 time:month ?m;
                 time:year "{year}"^^xsd:gYear.
              OPTIONAL {{ ?wasteinstance owl:sameAs ?wikidataLink. }}
            }}
            GROUP BY ?wasteName ?wikidataLink ?m
            ORDER BY ?m ?wasteName
            """
    results = g.query(query)
    output = []
    for row in results:
        output.append({
            "wasteName": str(row[0]),
            "wikidataLink": str(row[1]) if row[1] is not None else "",
            "month": str(row[2]),
            "totalAmount": float(row[3])
        })
    return output


def format_waste_type(waste_type):
    waste_type_map = {
        "CDW": "Construction and Demolition Waste",
        "biomedicalWaste": "Biomedical Waste",
        "clothing": "Clothing",
        "glass": "Glass",
        "non-recyclable-waste": "Non Recyclable Waste",
        "organicFood": "Organic Food",
        "packagingProductsOfPlastics": "Packaging Products of Plastic",
        "wastePaper": "Waste Paper",
        "wasteContainer": "Waste Container",
        "horseBed": "Horse Bed"
    }
    return waste_type_map.get(waste_type, "Unknown Waste Type")


app.jinja_env.filters['format_waste'] = format_waste_type


def reverse_format_waste_type(formatted_waste_type):
    reverse_waste_type_map = {
        "Construction and Demolition Waste": "CDW",
        "Biomedical Waste": "biomedicalWaste",
        "Clothing": "clothing",
        "Glass": "glass",
        "Non Recyclable Waste": "non-recyclable-waste",
        "Organic Food": "organicFood",
        "Packaging Products of Plastic": "packagingProductsOfPlastics",
        "Waste Paper": "wastePaper",
        "Waste Container": "wasteContainer",
        "Horse Bed": "horseBed"
    }
    return reverse_waste_type_map.get(formatted_waste_type, formatted_waste_type)


def fetch_yearly_district_waste(year="2021"):
    """
    Fetches the total amount of waste for each district for a specified year.

    :param year: The year for which the waste data is to be fetched.
    """
    g = rdflib.Graph()
    g.parse("data/rdf-with-links.ttl", format="ttl")

    query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX nso: <http://madridwastemanagement.org/group01/ontology/>
            PREFIX wst: <http://www.disit.org/km4city/schema#>
            PREFIX time: <http://www.w3.org/2006/time#>

            SELECT ?districtName (SUM(xsd:float(?val)) AS ?totalAmount) ?year
            WHERE {{
              ?districtInstance a dbo:District ;
                                rdfs:label ?districtName;
                                wst:hasResidue ?wasteinstance.
              ?wasteinstance nso:hasTotal ?totalinstance.
              ?totalinstance nso:value ?val;
                             time:year ?year.
            FILTER (?year = "{year}"^^xsd:gYear)

            }}

            GROUP BY ?districtName
            ORDER BY ?year
            """
    results = g.query(query)
    output = []
    for row in results:
        output_dict = {
            "districtName": str(row[0]),
            "totalAmount": float(row[1]),
            "year": str(row[2]),
        }
        output.append(output_dict)
    return output


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
              OPTIONAL {{ ?district wdt:P2046 ?area}}.
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
                'area': result.get('area', {'value': '--'})['value'],
                'coordinates': result['coordinates']['value'],
                'name': result['label']['value']
            }
            output.append(output_dict)
            return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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


def fetch_waste_type_distribution(waste_type="CDW", year="2021", month="1"):
    """
    Fetches distribution data of a specific waste type (default: CDW) across all districts for a specified year (default: 2021).

    :param waste_type: The waste type to fetch data for, default is 'CDW'.
    :param year: The year for which the data is to be fetched, default is '2021'.
    """
    g = rdflib.Graph()
    g.parse("data/rdf-with-links.ttl", format="ttl")

    query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX nso: <http://madridwastemanagement.org/group01/ontology/>
        PREFIX wst: <http://www.disit.org/km4city/schema#>
        PREFIX time: <http://www.w3.org/2006/time#>

        SELECT ?districtName ?amount 
        WHERE {{
            ?district a dbo:District ;
                      rdfs:label ?districtName ;
                      wst:hasResidue ?wasteinstance.
            ?wasteinstance rdfs:label "{waste_type}" ;
                           nso:hasTotal ?total.
            ?total nso:value ?amount ;
                   time:year "{year}"^^xsd:gYear;
                   time:month  "{month}"^^xsd:gMonth .
        }}
        """
    print(f"Fetching distribution data for waste type: {waste_type}, year: {year}, month: {month}")
    results = g.query(query)
    distribution_data = []
    for row in results:
        distribution_data.append({
            "districtName": str(row[0]),
            "amount": float(row[1])
        })
    print(f"Distribution Data: {distribution_data}")
    return distribution_data


#######################################################################################################################################################
#######################################################################################################################################################
########################################################## Rooter ######### ###############################################33###########################
#######################################################################################################################################################


@app.route('/')
def index():
    initial_year = "2021"  # You can change this to the current year or any default year
    waste_data = fetch_yearly_district_waste(initial_year)
    return render_template('index.html', waste_data=waste_data)


@app.route('/updateIndexYear')
def update_year():
    selected_year = request.args.get('year', '2021')
    print(selected_year)
    waste_data = fetch_yearly_district_waste(selected_year)
    return render_template('index.html', waste_data=waste_data, selected_year=selected_year)


@app.route("/district")
def district():
    district_name = request.args.get("name")
    year = request.args.get("year", "2021")
    district_id = request.args.get("wikidataID")
    waste_results = run_sparql_query(district_name, year)
    district_details = run_district_details_query(district_id)
    return render_template("district.html", waste_results=waste_results, district_details=district_details,
                           selected_year=year)


@app.route("/wasteType")
def waste_type():
    wikidata_id = request.args.get("wikidata_id")
    waste_type_name = request.args.get("name", "Unknown Waste Type")
    formatted_waste_type_name = format_waste_type(waste_type_name)
    query_format_waste_type_name = reverse_format_waste_type(waste_type_name)
    waste_type_result = run_wasteType_query(wikidata_id)
    distribution_data = fetch_waste_type_distribution(query_format_waste_type_name)
    return render_template("wasteType.html", wasteType=formatted_waste_type_name, result=waste_type_result,
                           distribution=distribution_data)


@app.route("/updateWasteType")
def update_wasteType():
    wikidata_id = request.args.get("wikidata_id")
    waste_type_name = request.args.get("name", "Unknown Waste Type")
    year = request.args.get("year", "2021")
    month = request.args.get("month", "1")
    formatted_waste_type_name = format_waste_type(waste_type_name)
    query_format_waste_type_name = reverse_format_waste_type(waste_type_name)
    waste_type_result = run_wasteType_query(wikidata_id)
    distribution_data = fetch_waste_type_distribution(query_format_waste_type_name, year, month)
    return render_template("wasteType.html", wasteType=formatted_waste_type_name, result=waste_type_result,
                           distribution=distribution_data, year=year, month=month)


if __name__ == "__main__":
    app.run(debug=True)
