import csv

from django.http import JsonResponse
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal, XSD


def listar_puntos_desfibrilador(request):
    # Crear un grafo RDF y cargar los datos desde tu propio archivo RDF
    g = Graph().parse("resultado.rdf", format="turtle")  # Reemplaza 'ruta_a_tu_archivo.rdf' por la ubicación de tu RDF

    # Definir el espacio de nombres de tu ontología
    ns = Namespace("http://ext.defibrilator/ontology#")

    # Obtener los parámetros de la consulta GET
    placeType = request.GET.get('placeType')
    municipalidadCodigo = request.GET.get('municipalidadCodigo')

    # Construir la consulta SELECT en función de los parámetros proporcionados
    query = '''
        SELECT ?type ?latitude ?longitude ?openingHours ?name ?address
        WHERE {
            ?desfibrillator rdf:type ns:Defibrillator.
            ?desfibrillator ns:placeType ?type.
            ?desfibrillator ns:latitude ?latitude.
            ?desfibrillator ns:longitude ?longitude.
            ?desfibrillator ns:openingHours ?openingHours.
            ?desfibrillator ns:name ?name.
            ?desfibrillator ns:address ?address.
    '''

    if placeType:
        query += f'FILTER (?type = "{placeType}")'

    if municipalidadCodigo:
        query += f'?desfibrillator ns:belongsToMunicipality <http://ext.defibrilator/resource/Municipality/{municipalidadCodigo}> .'

    query += '}'

    # Ejecutar la consulta SELECT en el grafo RDF
    results = g.query(query, initNs={"ns": ns})

    # Crear una lista para almacenar los datos de los desfibriladores
    puntos_desfibrilador = []

    # Recorrer los resultados e incluirlos en la lista como diccionarios
    for row in results:
        tipo, latitud, longitud, horario, nombre, direccion = row
        puntos_desfibrilador.append({
            "type": str(tipo),
            "latitude": str(latitud),
            "longitude": str(longitud),
            "openingHours": str(horario),
            "name": str(nombre),
            "address": str(direccion)
        })

    return JsonResponse({"puntos_desfibrilador": puntos_desfibrilador})


def listar_municipalidades(request):
    # Crear un grafo RDF y cargar los datos desde tu propio archivo RDF
    g = Graph().parse("resultado.rdf", format="turtle")  # Reemplaza 'ruta_a_tu_archivo.rdf' por la ubicación de tu RDF

    # Definir el espacio de nombres de tu ontología
    ns = Namespace("http://ext.defibrilator/ontology#")

    # Preparar la consulta SPARQL para obtener las municipalidades
    query = f'''
        SELECT ?municipalityCode ?municipalityName
        WHERE {{
            ?municipality a ns:Municipality;
                ns:code ?municipalityCode;
                ns:name ?municipalityName.
        }}
    '''

    # Ejecutar la consulta SPARQL en el grafo RDF
    results = g.query(query, initNs={"ns": ns})

    # Crear una lista de diccionarios para almacenar los datos de las municipalidades
    municipalidades = []

    # Recorrer los resultados e incluirlos en la lista de diccionarios
    for row in results:
        municipality_code, municipality_name = row
        municipalidades.append({
            "code": str(municipality_code),
            "name": str(municipality_name)
        })

    return JsonResponse({"municipalidades": municipalidades})


def listar_tipos_placeType(request):
    # Crear un grafo RDF y cargar los datos desde tu propio archivo RDF
    g = Graph().parse("resultado.rdf", format="turtle")  # Reemplaza 'ruta_a_tu_archivo.rdf' por la ubicación de tu RDF

    # Definir el espacio de nombres de tu ontología
    ns = Namespace("http://ext.defibrilator/ontology#")

    # Preparar la consulta SPARQL para obtener los tipos de placeType
    query = f'''
        SELECT DISTINCT ?placeType
        WHERE {{
            ?desfibrillator a ns:Defibrillator;
                ns:placeType ?placeType.
        }}
    '''

    # Ejecutar la consulta SPARQL en el grafo RDF
    results = g.query(query, initNs={"ns": ns})

    # Crear una lista para almacenar los tipos de placeType
    tipos_placeType = []

    # Recorrer los resultados e incluirlos en la lista
    for row in results:
        place_type = row[0]
        tipos_placeType.append(str(place_type))

    return JsonResponse({"tipos_placeType": tipos_placeType})
