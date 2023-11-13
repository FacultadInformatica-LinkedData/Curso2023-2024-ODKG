from rdflib import Graph, Namespace, RDFS
from rdflib.plugins.sparql import prepareQuery

g = Graph()
filename = "rdf_graph-with-links.ttl"
g.parse(filename, format="ttl")

ns = Namespace("https://barca_environmental_monitoring.es/")
g.namespace_manager.bind('ns', ns, override=False)


def execute_query(query):
    result = prepareQuery(query, initNs={"rdfs": RDFS, "ns": ns})
    return g.query(result)


def all_cabins():
    query = """
    SELECT ?number ?latitude ?longitude
    WHERE {
        ?cabin rdf:type ns:AirQualityCabin .
        ?cabin ns:cabinNumber ?number .
        ?cabin ns:cabinLatitude ?latitude .
        ?cabin ns:cabinLongitude ?longitude .
    }
    """

    cabin_results = execute_query(query)
    latitudes, longitudes, texts = [], [], []
    for r in cabin_results:
        latitudes.append(float(r.latitude))
        longitudes.append(float(r.longitude))
        texts.append(r.number)
    return latitudes, longitudes, texts


def cabins_which_measure_contaminants(contaminant):
    query = """
    SELECT ?number ?latitude ?longitude
    WHERE {
        ?cabin rdf:type ns:AirQualityCabin .
        ?cabin ns:cabinNumber ?number .
        ?cabin ns:cabinLatitude ?latitude .
        ?cabin ns:cabinLongitude ?longitude .
        ?cabin ns:hasMeasured ?contaminant .
        ?contaminant ns:contaminantName ?contaminant_name .
        FILTER(?contaminant_name = "%s")
    }
    """ % contaminant

    cabin_results = execute_query(query)
    latitudes, longitudes, texts = [], [], []
    for r in cabin_results:
        latitudes.append(float(r.latitude))
        longitudes.append(float(r.longitude))
        texts.append(r.number)
    return latitudes, longitudes, texts


def cabins_in_neighbourhoods_with_populations_bigger_than(threshold):
    query = """
    SELECT ?number ?latitude ?longitude
    WHERE {
        ?cabin rdf:type ns:AirQualityCabin .
        ?cabin ns:cabinNumber ?number .
        ?cabin ns:cabinLatitude ?latitude .
        ?cabin ns:cabinLongitude ?longitude .
        ?cabin ns:stationedAt ?address .
        ?address ns:inNeighbourhood ?neighbourhood .
        ?neighbourhood ns:neighbourhoodPopulation ?population .
        FILTER(?population > %s)
    }
    """ % threshold

    tree_results = execute_query(query)
    latitudes, longitudes, texts = [], [], []
    for r in tree_results:
        latitudes.append(float(r.latitude))
        longitudes.append(float(r.longitude))
        texts.append(r.number)
    return latitudes, longitudes, texts


if __name__ == "__main__":
    results = cabins_in_neighbourhoods_with_populations_bigger_than(1000)
    print(results)
