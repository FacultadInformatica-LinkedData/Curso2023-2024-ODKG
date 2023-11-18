from rdflib import Graph, Namespace

from functools import lru_cache


DATA_FILE_PATH = "museum_api/data/dataset-with-links-updated.ttl"

NAMESPACES = {
    "art": Namespace("http://artwork.org/"),
    "owl": Namespace("http://www.w3.org/2002/07/owl/"),
    "own": Namespace("https://soum2111.github.io/"),
    "sch": Namespace("https://schema.org/"),
}
@lru_cache
def get_data_graph_object() -> Graph:
    graph = Graph()

    for namespace_prefix, namespace_link in NAMESPACES.items():
        graph.bind(namespace_prefix, namespace_link)

    return graph.parse(DATA_FILE_PATH, format='ttl')
