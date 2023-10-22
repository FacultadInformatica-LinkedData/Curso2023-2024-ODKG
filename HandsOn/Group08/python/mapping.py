from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib import Graph, Namespace
from rdflib.query import Result
import morph_kgc


def dump2json(filename:str, result:Result):
     with open(filename+"result.csv", "wb") as f:
        f.write(result.serialize(format="csv"))

# PATHS

QUERYS_SPARQL = "rdf/queries.sparql"
CONFIG_MAPPING = "mappings/config.ini"
OUT_QUERY = "rdf/query-"
OUT_GRAPH = "rdf/University.ttl"

#  Namespaces
NS = Namespace(
    'http://www.semanticweb.org/upm/opendata/group08/ontologies/ns#')
SCHEMA = Namespace("https://schema.org/")
DBO = Namespace("https://dbpedia.org/ontology/")
DBP = Namespace("https://dbpedia.org/page/")

INIT_NS = {"ns": NS, "dbo": DBO, "rdf": RDF}
# Crear grafo en formato RDF

print(RDF)

with open(CONFIG_MAPPING) as f:
    config = f.read()

g = morph_kgc.materialize(config)

g.namespace_manager.bind('ns', Namespace(
    "http://www.semanticweb.org/upm/opendata/group08/ontologies/ns#"), override=False)
g.namespace_manager.bind('schema', Namespace(
    "https://schema.org/"), override=False)


# Binding the prefixes
g.bind('rdfs', RDFS)
g.bind('ns', NS)
g.bind('foaf', FOAF)
g.bind('rdf', RDF)
g.bind('dbo', DBO)
g.bind('dbp', DBP)
g.bind('schema', SCHEMA)

queries = ""

# Query 1:

queries += """\n# Query 1: Select all the possible values of the property 
# dbo:city of the entities that belong to class n:University \n"""


query_text = """    
    SELECT ?individual ?value WHERE {
        ?individual dbo:city ?value .
        ?individual rdf:type ns:University.
    }    
"""


queries += query_text

results_q1 = g.query(prepareQuery(query_text, initNs=INIT_NS))

dump2json(OUT_QUERY+"1", results_q1)


# Query 2 :
queries += """\n#Query 2: Select all the values and years of all the Liberal Arts Colleges"""

query_text2 = """    
    SELECT ?value ?year WHERE {
        ?ranking ns:score ?value.
        ?ranking ns:yearPublished ?year.
        ?individual ns:hasLiberalArtsRanking  ?ranking .
        ?individual rdf:type ns:University.
    }    
"""

queries += query_text2

results_q2 = g.query(prepareQuery(query_text2, initNs=INIT_NS))

dump2json(OUT_QUERY+"2", results_q2)

# Query 3:

queries += "\n#Query 3: Select the values of admission rate of all the entities of type University"

#        ?unversity ns:name ?name .
query_text3 = """    
    SELECT ?name ?value WHERE {
        ?university rdf:type ns:University .

        ?university ns:hasAdmisionRate ?rate .
        ?rate ns:value ?value
    }    
"""

queries += query_text3


results_q3 = g.query(prepareQuery(query_text3, initNs=INIT_NS))


dump2json(OUT_QUERY+"3", results_q3)

# Write queries
with open(QUERYS_SPARQL, "w") as f:
    f.write(queries)

# Write Ontology
with open(OUT_GRAPH, "w") as f:
     f.write(g.serialize(format="turtle"))
