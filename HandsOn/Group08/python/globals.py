from os.path import join

OUT_GRAPH = join("rdf", "UniversityInformation.nt")
OUT_GRAPH_LINKS = join("rdf", "UniversityInformation-with-links.ttl")
OUT_GRAPH_UPDATED = join("rdf", "UniversityInformation-updated.ttl")

CONFIG_MAPPING = join("mappings", "config.ini")
CONFIG_MAPPING_LINKS = join("mappings", "config-with-links.ini")
CONFIG_MAPPING_UPDATED = join("mappings", "config-updated.ini")

QUERYS_SPARQL = join("rdf", "queries.sparql")
QUERYS_SPARQL_LINKS = join("rdf", "queries-with-links.sparql")

OUT_QUERY = join("rdf", "query")


def change_path(filename): return filename.replace(
    "-updated.csv", "-final.csv")


BASE_PATH = "csv"
UNIVERISTY_INFO = join(BASE_PATH, "us-colleges-and-universities-updated.csv")
UNIVERITY_RATES = join(BASE_PATH, "IPEDS-data-updated.csv")
COLLEGE_RANKING = join(
    BASE_PATH, "US-News-Rankings-Liberal-Arts-Colleges-Through-2023-updated.csv")
UNIVERSITY_ARTS_RANKING = join(
    BASE_PATH, "US-News-Rankings-Universities-Through-2023-updated.csv")
