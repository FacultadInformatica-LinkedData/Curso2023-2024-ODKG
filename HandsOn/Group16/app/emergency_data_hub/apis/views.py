import os

from django.http import JsonResponse
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal, XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import sys


def listar_desfibriladores(request):
    placeType = request.GET.get("placeType")
    municipalidadcodigo = request.GET.get("municipalidadCodigo")

    endpoint_wikidata_url = "https://query.wikidata.org/sparql"
    endpoint_local = "http://localhost:3030/desfibriladores/sparql"
    desfibriladores = []
    query = '''
    PREFIX ns1: <http://upm.defibrillator.com/ontology/municipality#>
    PREFIX ns2: <http://upm.defibrillator.com/ontology/defibrillator#>
    PREFIX ns3: <https://www.wikidata.org/>
    
    SELECT ?address ?coordinate_x ?coordinate_y ?dea_code ?establishment_type ?location ?ownership_type ?postal_code ?municipality_code ?municipality ?municipality_name ?wikidata_link
    WHERE {{
        ?defibrillator a ns2:Defibrillator ;
                       ns2:address ?address ;
                       ns2:coordinate_x ?coordinate_x ;
                       ns2:coordinate_y ?coordinate_y ;
                       ns2:dea_code ?dea_code ;
                       ns2:establishment_type ?establishment_type ;
                       ns2:location ?location ;
                       ns2:ownership_type ?ownership_type ;
                       ns2:postal_code ?postal_code ;
                       ns1:belongsToMunicipality ?municipality ;
                       ns1:municipality_code ?municipality_code .
        
        ?municipality ns1:municipality_name ?municipality_name ;
                     ns3:wikidata_link ?wikidata_link .
    
        FILTER (?establishment_type = "{}" && ?municipality_code = "{}").
    }}

    '''
    query = query.format(placeType, municipalidadcodigo)
    print("############################## START GET Defibrillator")
    print(query)
    print("############################## END GET Defibrillator")
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_local, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    muncipality_data = {}
    if (len(results.get('results')['bindings']) > 0):
        parts = results.get('results')['bindings'][0].get('wikidata_link')['value'].split("/")
        mucipality_code = parts[-1]
        muncipality_data = {
            "postal_code": results.get('results')['bindings'][0].get('postal_code')['value'],
            "municipality_code": results.get('results')['bindings'][0].get('municipality_code')['value'],
            "wikidata_link": results.get('results')['bindings'][0].get('wikidata_link')['value'],
            "municipality_name": results.get('results')['bindings'][0].get('municipality_name')['value'],
            "wiki_data": get_extra_data(endpoint_wikidata_url, mucipality_code),
            "hospital": get_hospital(endpoint_wikidata_url, mucipality_code),
            "desfibriladores": []
        }
        for row in results.get('results')['bindings']:
            muncipality_data["desfibriladores"].append({
                "address": row['address']['value'],
                "coordinate_x": row['coordinate_x']['value'],
                "coordinate_y": row['coordinate_y']['value'],
                "dea_code": row['dea_code']['value'],
                "establishment_type": row['establishment_type']['value'],
                "location": row['location']['value'],
                "ownership_type": row['ownership_type']['value'],
                "municipality_link": row['wikidata_link']['value'],
            })
    return JsonResponse({"municipality": muncipality_data})


def get_extra_data(endpoint_url, muncipality_code):
    query_template = """PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        SELECT ?web
        WHERE {{
          wd:{} wdt:P856 ?web.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}"""
    query = query_template.format(muncipality_code)
    print("############################## START GET Extra data for Municipality")
    print(query)
    print("############################## END GET Extra data for Municipality")
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


def get_hospital(endpoint_url, municipality_code):
    query_template = """

    SELECT DISTINCT ?hospitals ?hospitalsLabel 
        WHERE
        {{
          VALUES ?tipo {{ wd:Q569500 wd:Q16917 wd:Q5755377 wd:Q210999 wd:Q4287745 }}
          OPTIONAL {{ ?hospitals wdt:P31 ?tipo. }}
          ?hospitals wdt:P131 wd:{}  
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}      
        }}
    """.format(municipality_code)
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    print("############################## START GET Hospital")
    print(query_template)
    print("############################## END GET Hospital")
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query_template)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


def listar_municipalidades(request):
    endpoint_local = "http://localhost:3030/desfibriladores/sparql"
    municipalidades = []
    query = '''
        PREFIX ns: <http://upm.defibrillator.com/ontology/municipality#>
        SELECT DISTINCT ?municipalityCode ?municipalityName
        WHERE {
            ?municipality a ns:Municipality;
                ns:municipality_name ?municipalityName.
            BIND(STRAFTER(str(?municipality), "Municipality/") as ?municipalityCode)
        }
        ORDER BY ?municipalityName
    '''

    print("##################################")
    print("query for list municipality")
    print(query)
    print("##################################")

    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_local, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        municipalidades.append(
            {'code': result['municipalityCode']['value'], 'value': result['municipalityName']['value']})

    return JsonResponse({"municipalidades": municipalidades})


def listar_tipos_placeType(request):
    endpoint_local = "http://localhost:3030/desfibriladores/sparql"
    tipos_placeType = []
    query_template = """
        PREFIX ns: <http://upm.defibrillator.com/ontology/defibrillator#>
        SELECT DISTINCT ?establishment_type
        WHERE {
            ?desfibrillator a ns:Defibrillator;
            ns:establishment_type ?establishment_type.
        }
        ORDER BY ?establishment_type
    """
    print("##################################")
    print("query for list establishment_type")
    print(query_template)
    print("##################################")

    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_local, agent=user_agent)
    sparql.setQuery(query_template)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        tipos_placeType.append(str(result["establishment_type"]["value"]))
    return JsonResponse({"tipos_placeType": tipos_placeType})


def generate_rdf(request):
    # Definir tus URIs y Prefijos
    def_ontology = Namespace("http://ext.defibrilator/ontology#")
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
    ext_defibrilator = Namespace("http://example.com/resource/")
    ext_municipality = Namespace("http://ext.defibrilator/resource/Municipality/")

    # Crear un nuevo grafo RDF
    g = Graph()

    # Cargar la ontología
    g.parse("apis/ontology.ttl", format="ttl")

    # Abrir y leer el archivo CSV
    with open("desfibriladores_old.csv", "r") as csv_file:
        next(csv_file)  # Saltar la primera línea si contiene encabezados
        for line in csv_file:
            values = line.strip().split(",")
            if len(values) == 11:
                # Crear URIs para cada entidad
                building_uri = ext_defibrilator[values[-1]]
                municipality_uri = ext_municipality[values[2]]

                # Agregar triples al grafo
                g.add((building_uri, RDF.type, def_ontology["Defibrillator"]))
                g.add((building_uri, def_ontology["address"], Literal(values[4], datatype=XSD.string)))
                g.add((building_uri, def_ontology["belongsToMunicipality"], municipality_uri))
                g.add((building_uri, def_ontology["latitude"], Literal(float(values[8]), datatype=XSD.float)))
                g.add((building_uri, def_ontology["longitude"], Literal(float(values[7]), datatype=XSD.float)))
                g.add((building_uri, def_ontology["name"], Literal(values[10], datatype=XSD.string)))
                g.add((building_uri, def_ontology["openingHours"], Literal(values[9], datatype=XSD.string)))
                g.add((building_uri, def_ontology["placeType"], Literal(values[0], datatype=XSD.string)))

                g.add((municipality_uri, RDF.type, def_ontology["Municipality"]))
                g.add((municipality_uri, def_ontology["code"], Literal(values[2], datatype=XSD.string)))
                g.add((municipality_uri, def_ontology["name"], Literal(values[3], datatype=XSD.string)))

                # Serializar y guardar el grafo RDF
    # g.serialize("final_output.rdf", format="xml")
    g.serialize("final_output.rdf", format="turtle")


def generate_ttl_from_nt(request):
    input_nt_file = "result.nt"
    output_ttl_file = "result.ttl"

    g = Graph()
    g.parse(input_nt_file, format="nt")

    g.serialize(destination=output_ttl_file, format="turtle")
