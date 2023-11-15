from typing import List, Tuple

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


def cabins_which_measure_contaminants(contaminant: str) -> List[Tuple[float, float, str, str]]:
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

    query2 = """
    SELECT DISTINCT ?unit ?effect ?mass
    WHERE {
        ?contaminant ns:contaminantName ?contaminant_name .
        ?contaminant ns:unit ?unit .
        ?contaminant ns:effect ?effect .
        ?contaminant ns:mass ?mass .
        FILTER(?contaminant_name = "%s")
    }
    """ % contaminant
    contam_result = execute_query(query2)
    for r in contam_result:
        unit, effect, mass = r.unit, r.effect, r.mass
        break

    info = f"Contaminant: {contaminant}\nUnit: {unit}\nEffect: {effect}\nAtomic mass: {mass}"
    return latitudes, longitudes, texts, info


def cabins_in_neighbourhoods_with_populations_bigger_than(threshold: int) -> List[Tuple[float, float, str]]:
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


def temperature_data(start: int, end: int, month: str) -> List[Tuple[int, float]]:
    query = """
    SELECT ?year ?measurement
    WHERE {
        ?temperature rdf:type ns:Temperature .
        ?temperature ns:temperature ?measurement .
        ?temperature ns:year ?year .
        ?temperature ns:month ?month .
        FILTER(?year >= %s && ?year <= %s && ?month = "%s")
    }
    """ % (start, end, month)
    results = execute_query(query)
    return [(int(r.year), float(r.measurement)) for r in results]
