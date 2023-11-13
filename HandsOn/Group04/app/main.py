from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Cargar el archivo .ttl al grafo RDF
graph = Graph()
graph.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")
geonames = Namespace("http://www.geonames.org/ontology#")
esadm = Namespace("http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#")


@app.route('/')
def home():
    result = get_event_list()
    prices = get_prices()
    accessibilities = get_accessibilities()
    districts = get_districts()
    return render_template('index.html', result=result, prices=prices, accessibilities=accessibilities, districts=districts)

def execute_sparql_query(query):
    results = graph.query(query, initNs={"ns": ns, "schema": schema, "geonames": geonames, "esadm": esadm})

    result_values = []
    for row in results:
        result_row = []
        for value in row:
            result_row.append(value.toPython() if hasattr(value, 'toPython') else value)
        result_values.append(result_row)

    return result_values

def get_event_list(search_value=""):
    query = f"""
     SELECT ?event ?name ?description ?eventPrice ?eventAccessibility ?facilityName ?eventPlace ?startDate ?endDate ?audienceType ?eventType WHERE {{
        ?event a schema:Event ;
            schema:name ?name ;
            schema:description ?description ;
            ns:price ?eventPrice ;
            ns:accesibility ?eventAccessibility ;
            ns:hasPlace ?eventPlace ;
            schema:startDate ?startDate ;
            schema:endDate ?endDate ;
            ns:hasAudienceType ?audienceType ;
            ns:hasEventType ?eventType .
        ?eventPlace a ns:Facility ;
            ns:facilityName ?facilityName .
        FILTER (CONTAINS(?name, "{search_value}"))
    }}
    """
    result = execute_sparql_query(query)
    return result

def get_prices():
    query = '''
    SELECT DISTINCT ?price
    WHERE {
        ?event a schema:Event ;
            ns:price ?price .
    }
    '''
    # Almacena los resultados en una lista
    prices_list = [row.price for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    # Visualiza los resultados
    # print("Precios:", prices_list)
    return prices_list


def get_districts():
    query = '''
    SELECT DISTINCT ?district
    WHERE {
        ?address a ns:Address ;
               ns:belongsTo ?district ;
      }
    '''
    # Almacena los resultados en una lista
    districts_list = [row.district for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    # Visualiza los resultados
    # print("Districts:", districts_list)
    return districts_list

def get_accessibilities():
    query = '''
    SELECT DISTINCT ?accessibility
    WHERE {
        ?event a schema:Event ;
            ns:accesibility ?accessibility .
    }
    '''
    # Almacena los resultados en una lista
    accessibility_list = [row.accessibility for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    # Combina todas las cadenas en una sola
    combined_accessibility = ",".join(accessibility_list)

    # Divide la cadena combinada en elementos únicos
    unique_accessibility = set(combined_accessibility.split(','))

    # Visualiza los resultados
    # print("Accessibility:", list(unique_accessibility))
    return list(unique_accessibility)

@app.route('/search')
def search():
    search_value = request.args.get('search_value', '')
    result_list = get_event_list(search_value)
    prices = get_prices()
    accessibilities = get_accessibilities()
    districts = get_districts()
    return render_template('index.html', result=result_list, prices=prices, accessibilities=accessibilities, districts=districts)

@app.route('/get_facility_info')
def get_facility_info():
    facility_id = request.args.get('facility_id', '')
    facility = "http://www.madculturalevents.es/group04/resources/facility/" + facility_id

    query = f"""
     SELECT ?facilityName ?metro ?bus ?train ?url ?lat ?long ?street ?number ?districtName WHERE {{
            <{facility}> a ns:Facility ;
                ns:facilityName ?facilityName ;
                ns:metro ?metro ;
                ns:bus ?bus ;
                ns:train ?train ;
                ns:facilityUrl ?url ;
                ns:ubicatedIn ?geometry ;
                ns:hasAddress ?address .
            ?geometry ns:hasLat ?lat ;
                ns:hasLong ?long .
            ?address ns:addressName ?street ;
                ns:number ?number;
                ns:belongsTo ?district .
            ?district geonames:officialName ?districtName .
    }}
    """
    result = execute_sparql_query(query)

    query = f"""
    SELECT ?event ?name ?description ?eventPrice ?eventAccessibility ?facilityName ?eventPlace ?startDate ?endDate ?audienceType ?eventType WHERE {{
        ?event a schema:Event ;
            schema:name ?name ;
            schema:description ?description ;
            ns:price ?eventPrice ;
            ns:accesibility ?eventAccessibility ;
            ns:hasPlace ?eventPlace ;
            schema:startDate ?startDate ;
            schema:endDate ?endDate ;
            ns:hasAudienceType ?audienceType ;
            ns:hasEventType ?eventType ;
            ns:hasPlace <{facility}> .
    }}
    """
    events = execute_sparql_query(query)

    return render_template('facility_info.html', result=result[0], events=events)


if __name__ == '__main__':
    app.run(debug=True)