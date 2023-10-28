from os.path import join

CONFIG_MAPPING = join("mappings", "config.ini")
OUT_GRAPH = join("rdf","UniversityInformation.nt")
QUERYS_SPARQL = join("rdf", "queries.sparql")
CONFIG_MAPPING = join("mappings", "config.ini")
OUT_QUERY = join("rdf", "query")


change_path = lambda filename: filename.replace("-updated.csv", "-final.csv")

BASE_PATH = "csv"
UNIVERISTY_INFO = join(BASE_PATH, "us-colleges-and-universities-updated.csv")
UNIVERITY_RATES = join(BASE_PATH, "IPEDS-data-updated.csv")
COLLEGE_RANKING = join(BASE_PATH, "US-News-Rankings-Liberal-Arts-Colleges-Through-2023-updated.csv")
UNIVERSITY_ARTS_RANKING = join(BASE_PATH, "US-News-Rankings-Universities-Through-2023-updated.csv")
