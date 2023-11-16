from flask import Flask, render_template, request
from rdflib import Graph, Namespace
import requests
from datetime import datetime

app = Flask(__name__)

# Cargar el archivo .ttl al grafo RDF
graph = Graph()
graph.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")
territorio = Namespace("http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#")
geonames = Namespace("http://www.geonames.org/ontology#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
wdt = Namespace("http://www.wikidata.org/prop/direct#")
wd=Namespace("http://www.wikidata.org/entity#")
xsd=Namespace("http://www.w3.org/2001/XMLSchema#")



@app.route('/')
def home():
    result = get_event_list()
    prices = get_prices()
    accessibilities = get_accessibilities()
    district_names = get_district_names()
    metro_list = get_metro_list()
    facility_names = get_facility_names()
    audience_types = get_audience_types()
    event_types = get_event_types()
    locations = get_locations(result)

    return render_template('index.html', result=result, prices=prices, accessibilities=accessibilities,
                           district_names=district_names, metro_list = metro_list, facility_names=facility_names, 
                           audience_types=audience_types, event_types=event_types, locations=locations)

@app.route('/search_filter')
def home_filter():
    StartDate = request.args.get('StartDate', '')
    EndDate = request.args.get('EndDate', '')
    price_select = request.args.get('price-select', '')
    district_select = request.args.get('district-select', '')
    transport_select = request.args.get('transport-select', '')
    facility_select = request.args.get('facility-select', '')
    accessibility_select = request.args.get('accessibility-select', '')
    event_type_select = request.args.get('event-type-select', '')
    audience_type_select = request.args.get('audience-type-select', '')
    if price_select!='?price':
        price_select=f'FILTER (?price = "{price_select}")'
    else:
        price_select=''

    if district_select !='?districtName':
        district_select=f"""
            ?eventPlace ns:hasAddress ?Address.
            ?Address a ns:Address;
                ns:belongsTo ?district .
            ?district geonames:officialName ?districtName .
            FILTER regex(?districtName, "{district_select}", "i")
        """
    else:
        district_select=''

    if transport_select !='?metro':
        transport_select=f"""
        ?eventPlace ns:metro ?metro .
        FILTER (?metro = "{transport_select}")
        """
    else:
        transport_select=''
    
    if facility_select != '?eventPlaceName':
        facility_select=f'FILTER regex(?facilityName, "{facility_select}", "i")'
    else:
        facility_select=''
    
    if accessibility_select!= '?eventAccessibility':
       accessibility_select =f'FILTER regex(?eventAccessibility, "{accessibility_select}", "i")'
    else:
        accessibility_select=''
    
    if event_type_select != '?EventType':
       event_type_select =f'FILTER regex(?eventType, "{event_type_select}", "i")'
    else:
        event_type_select=''
    
    if audience_type_select != '?AudienceType':
       audience_type_select =f'FILTER regex(?audienceType, "{audience_type_select}", "i")'
    else:
        audience_type_select=''


    if StartDate == '':
        StartDate = ''
    else:
        StartDate = f'FILTER (?startDate >= "{StartDate}T00:00:00.0"^^xsd:dateTime'

    if EndDate == '':
        EndDate = ')' if StartDate != '' else ''
    else:
        EndDate = f' && (?endDate <= "{EndDate}T23:59:59.0"^^xsd:dateTime))'
    
    query = f"""
    SELECT ?event ?name ?description ?price ?eventAccessibility ?facilityName ?eventPlace ?startDate ?endDate ?audienceType ?eventType WHERE {{
        ?event a schema:Event ;
            schema:name ?name ;
            schema:description ?description ;
            ns:price ?price ;
            ns:accesibility ?eventAccessibility ;
            ns:hasPlace ?eventPlace ;
            schema:startDate ?startDate ;
            schema:endDate ?endDate ;
            ns:hasAudienceType ?audienceType ;
            ns:hasEventType ?eventType .
        ?eventPlace a ns:Facility ;
            ns:facilityName ?facilityName .
        {transport_select}
        {price_select}
        {accessibility_select}
        {audience_type_select}
        {event_type_select}
        {facility_select}
        {StartDate}
        {EndDate}
        {district_select}
    }}
    """
    print(query)
    result = execute_sparql_query(query)
    locations = get_locations(result)
    prices = get_prices()
    accessibilities = get_accessibilities()
    district_names = get_district_names()
    metro_list = get_metro_list()
    facility_names = get_facility_names()
    audience_types = get_audience_types()
    event_types = get_event_types()

    return render_template('index.html', result=result, prices=prices, accessibilities=accessibilities,
                           district_names=district_names, metro_list = metro_list, facility_names=facility_names, 
                           audience_types=audience_types, event_types=event_types, locations=locations)

def execute_sparql_query(query):
    results = graph.query(query, initNs={"ns": ns, "schema": schema, "geonames": geonames, "territorio": territorio,"wdt":wdt,"wd":wd,"xsd":xsd})

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
        FILTER regex(?name, "{search_value}", "i")
    }}
    """
    print(search_value)
    
    result = execute_sparql_query(query)
    return result



def get_locations(results):
    wikidata_query = 'https://query.wikidata.org/embed.html#%23defaultView%3AMap%0ASELECT%20*%20WHERE%20%7B%20'

    i = 1
    for event in results:
        # print(event[0])
        query = f'''
        SELECT ?sameAs
        WHERE {{
            <{event[0]}> a schema:Event ;
            ns:hasPlace ?place .
            ?place ns:hasAddress ?address .
            ?address owl:sameAs ?sameAs
        }}
        '''
        locations = [row.sameAs for row in graph.query(query, initNs={"ns": ns, "schema": schema, "owl": owl})]


        for row in locations:
            if row is not None:
                same_as_url = row
                wikidata_id = same_as_url.split("/")[-1]
                if wikidata_id:
                    wikidata_query+=f'%0A%20%20OPTIONAL%20%7B%20wd%3A{wikidata_id}%20wdt%3AP625%20%3Fgeo{i}%20%7D'
                    i += 1

    wikidata_query+='%0A%7D'

    return wikidata_query





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
       ?event a schema:Event ;
            ns:hasPlace ?facility .
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
    result_list = get_event_list(search_value)
    prices = get_prices()
    accessibilities = get_accessibilities()
    district_names = get_district_names()
    metro_list = get_metro_list()
    facility_names = get_facility_names()
    audience_types = get_audience_types()
    event_types = get_event_types()
    locations = get_locations(result_list)
    return render_template('index.html', result=result_list, prices=prices, accessibilities=accessibilities,
                           district_names=district_names, metro_list = metro_list, facility_names=facility_names, 
                           audience_types=audience_types, event_types=event_types, locations=locations)

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

    query_wikiID = f"""
    SELECT distinct ?wikiID WHERE {{
        ?District  a territorio:Distrito ; 
            geonames:officialName "{result[0][9]}"^^xsd:string;
            owl:sameAs ?wikiID.
    }}
    """
    wikiURIID=execute_sparql_query(query_wikiID)

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
    wikiID=str(wikiURIID[0][0]).split("/")[-1]
    url = 'https://query.wikidata.org/sparql'
    query2 = f"""
    SELECT distinct ?image WHERE {{
    wd:{wikiID} wdt:P18 ?image
    }}
    """
    r = requests.get(url, params = {'format': 'json', 'query': query2})
    data = r.json()
    
    if data["results"]["bindings"]:
        image_url=data["results"]["bindings"][0]["image"]['value']
    else:
        image_url=''

    return render_template('facility_info.html', result=result[0], events=events,image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)