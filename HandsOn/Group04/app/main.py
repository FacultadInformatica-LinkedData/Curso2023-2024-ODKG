from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Cargar el archivo .ttl al grafo RDF
graph = Graph()
graph.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")
territorio = Namespace("http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#")
geonames = Namespace("http://www.geonames.org/ontology#")

@app.route('/')
def home():
    query = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX schema: <http://schema.org/> 
    SELECT ?name ?eventPrice ?eventAccessibility ?eventPlace WHERE {
      ?event a schema:Event ;
               schema:name ?name ;
               ns0:price ?eventPrice ;
               ns0:accesibility ?eventAccessibility ;
               ns0:hasPlace ?eventPlace  .
    }
    """
    result = execute_sparql_query(query)
    prices = get_prices()
    accessibilities = get_accessibilities()
    district_names = get_district_names()
    metro_list = get_metro_list()
    facility_names = get_facility_names()
    audience_types = get_audience_types()
    event_types = get_event_types()
    return render_template('index.html', query=query, result=result, prices=prices, accessibilities=accessibilities,
                           district_names=district_names, metro_list = metro_list, facility_names=facility_names, audience_types=audience_types, event_types=event_types)

def execute_sparql_query(query):
    results = graph.query(query)

    result_values = []
    for row in results:
        result_row = []
        for value in row:
            result_row.append(value.toPython() if hasattr(value, 'toPython') else value)
        result_values.append(result_row)

    return result_values

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

    return prices_list

def get_audience_types():
    query = '''
    SELECT DISTINCT ?audienceType
    WHERE {
        ?event a schema:Event ;
            ns:hasAudienceType ?audienceType .
    }
    '''
    # Almacena los resultados en una lista
    audience_types = [row.audienceType for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    # Combina todas las cadenas en una sola
    combined_audience_type = ",".join(audience_types)

    # Divide la cadena combinada en elementos únicos
    unique_audience_type = set(combined_audience_type.split(','))

    return list(unique_audience_type)


def get_event_types():
    query = '''
    SELECT DISTINCT ?eventType
    WHERE {
        ?event a schema:Event ;
            ns:hasEventType ?eventType .
    }
    '''
    # Almacena los resultados en una lista
    event_types = [row.eventType for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    return event_types


def get_district_names():
   query = '''
   SELECT DISTINCT ?districtName
   WHERE {
       ?district a territorio:Distrito ;
              geonames:officialName ?districtName .
   }
   '''

   # Almacena los resultados en una lista
   district_names = [row.districtName for row in graph.query(query, initNs={"ns": ns, "schema": schema, "territorio": territorio, "geonames": geonames})]

   return district_names

def get_metro_list():
   query = '''
   SELECT DISTINCT ?metro
   WHERE {
       ?facility a ns:Facility ;
              ns:metro ?metro .
   }
   '''

   # Almacena los resultados en una lista
   metro_list = [row.metro for row in graph.query(query, initNs={"ns": ns, "schema": schema})]
   
   return metro_list

def get_facility_names():
   query = '''
   SELECT DISTINCT ?facilityName
   WHERE {
       ?facility a ns:Facility ;
              ns:facilityName ?facilityName .
   }
   '''

   # Almacena los resultados en una lista
   facility_names = [row.facilityName for row in graph.query(query, initNs={"ns": ns, "schema": schema})]
   
   return facility_names

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

    return list(unique_accessibility)

@app.route('/search')
def search():
    search_value = request.args.get('search_value', '')
    q1 = f"""
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX schema: <http://schema.org/> 

    SELECT ?name ?eventPrice ?eventAccessibility ?eventPlace WHERE {{
        ?event a schema:Event .
        ?event schema:name ?name .
        ?event ns0:price ?eventPrice .
        ?event ns0:accesibility ?eventAccessibility .
        ?event ns0:hasPlace ?eventPlace .
        FILTER (CONTAINS(?name, "{search_value}"))
    }}
    """
    result = execute_sparql_query(q1)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)