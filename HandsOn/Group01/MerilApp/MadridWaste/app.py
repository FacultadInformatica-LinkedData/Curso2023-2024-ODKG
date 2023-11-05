from flask import Flask, render_template, request
import rdflib


#######################################################################################################################################################
#######################################################################################################################################################
########################################################## Environment ###############################################33###########################
#######################################################################################################################################################


app = Flask(__name__)

# Local database
g = rdflib.Graph()
g.parse("/home/meril/Documents/UPM/Curso2023-2024-ODKG/HandsOn/Group01/rdf/rdf-with-links.ttl", format="ttl")


#######################################################################################################################################################
#######################################################################################################################################################
########################################################## SPARQLE Queries ###############################################33###########################
#######################################################################################################################################################
def run_sparql_query(district_name):
    """
        Given an dsitrict name it generates th waste amount for each type of waste for each month
        :param district_name:
        :return:
        """
    g = rdflib.Graph()
    g.parse("/home/meril/Documents/UPM/Curso2023-2024-ODKG/HandsOn/Group01/rdf/rdf-with-links.ttl", format="ttl")

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
                                dbo:districtName "{district_name}";
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
            'wasteName': str(row[0]),
            'wikidataLink': str(row[1]),
            'month': str(row[2]),
            'totalAmount': str(row[3])
        }
        output.append(output_dict)
    return output


#######################################################################################################################################################
#######################################################################################################################################################
########################################################## Rooter ######### ###############################################33###########################
#######################################################################################################################################################


### If we end up with to many routes all the functions will be placed in separted folder called router or controler (MVC pattern)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/district')
def district():
    district_name = request.args.get('name')
    results = run_sparql_query(district_name)
    return render_template('district.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
