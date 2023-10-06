from django.http import JsonResponse
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, RDF, RDFS, Namespace


def example(request):
    nombres = []
    g = Graph().parse("http://www.w3.org/People/Berners-Lee/card")

    query = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?name
        WHERE {
            ?p rdf:type foaf:Person .

            ?p foaf:name ?name .
        }
    """

    results = g.query(query)

    print(len(results))
    for r in g.query(query):
        nombres.append(r["name"])
        print(r["name"])
    return JsonResponse({"names": nombres})


def politicians(request):
    nombres = []

    # Crear un grafo RDF y cargar los datos desde DBpedia
    g = Graph().parse("http://dbpedia.org/ontology/Politician")

    # Definir prefijos
    DBPEDIA = Namespace("http://dbpedia.org/ontology/")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")

    # Preparar la consulta SPARQL
    query = prepareQuery('''
        SELECT DISTINCT ?property ?name
        WHERE {
            ?politician rdf:type DBPEDIA:Politician.
            ?politician ?property ?value.
            ?politician FOAF:name ?name.
        }
        ''',
                         initNs={"DBPEDIA": DBPEDIA, "FOAF": FOAF}
                         )

    # Ejecutar la consulta en el grafo RDF
    results = g.query(query)

    # Recorrer los resultados e imprimirlos
    for row in results:
        property, name = row
        nombres.append(name)
        print(f"Property: {property}, Name: {name}")

    return JsonResponse({"names": nombres})
