from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.query import Result

from globals import OUT_GRAPH, OUT_QUERY, QUERYS_SPARQL
from pydantic import BaseModel
from typing import Optional

# Namespaces
SCHEMA = Namespace("https://schema.org/")
DBO = Namespace("https://dbpedia.org/ontology/")
DBP = Namespace("https://dbpedia.org/page/")

NS = Namespace(
    "http://www.semanticweb.org/upm/opendata/group08/ontology/UniversityInformation#")
RS = Namespace("http://www.semanticweb.org/upm/opendata/group08/resource/")

INIT_NS = {"ns": NS, "rs": RS, "dbo": DBO, "rdf": RDF}


class Query(BaseModel):
    id: int
    description: str
    query: str
    initBinding: Optional[dict] = {}


QUERIES = [
    Query(id=1, description="""Select all the possible values of the property
          # dbo:city of the entities that belong to class n:University """,
          query="""
            SELECT  DISTINCT ?nameCity ?uniname WHERE {
                ?university dbo:city ?city .
                ?city rdf:label ?nameCity.
                ?university rdf:type ns:University.
                ?university rdf:label ?uniname. 
        }    
    """),
    Query(id=2, description="""Select all the scores and years of all the Liberal Arts Colleges Rankings
          # for all the Universities located in the state of Florida)""",
          query="""
                    SELECT ?score ?year WHERE {
                        ?university rdf:type ns:University.
                        ?ranking ns:score ?score.
                        ?ranking ns:yearPublished ?year.
                        ?university ns:hasRanking  ?ranking .
                        ?ranking rdf:type ns:RankingUSNews.
                    } 
        """,
          initBinding={'?floridaname': Literal('FL', datatype=XSD.string)}),
    Query(id=3, description="Select the values of admission rate of all the entities of type University",
          query="""    
                    SELECT ?uniname ?enrollmentRate WHERE {
                        ?university rdf:type ns:University .
                        ?university rdf:label ?uniname. 
                        ?university ns:hasRate ?rate .
                        ?rate rdf:type ns:EnrollmentRate. 
                        ?rate ns:value ?enrollmentRate   
                    }    
                """
          ),
    Query(id=4, description="Retrieve the coordinates of the University which ranked first on the USNews Ranking",
          query="""    
                    SELECT ?longitude ?latitude WHERE {
                        ?university schema:longitude ?longitude .
                        ?university schema:latitude ?latitude .
                        ?university rdf:type ns:University .
                        ?university ns:hasRanking ?ranking .
                        ?ranking rdf:type ns:USNewsRanking .
                        ?ranking ns:score ?score
                    }    
                """,
          initBinding={'?score': Literal('1', datatype=XSD.string)}),
]


def dump2csv(filename: str, result: Result):
    with open(filename+"-result.csv", "wb") as f:
        f.write(result.serialize(format="csv"))


def make_query(query: Query, limit: int = 100):

    limit = "\nLIMIT " + str(limit)

    result = g.query(prepareQuery(query.query + limit, initNs=INIT_NS),
                     initBindings=query.initBinding)
    return result


if __name__ == "__main__":

    g = Graph()

    # Binding the prefixes
    g.bind('rdfs', RDFS)
    g.bind('ns', NS)
    g.bind('rs', RS)
    g.bind('foaf', FOAF)
    g.bind('rdf', RDF)
    g.bind('dbo', DBO)
    g.bind('dbp', DBP)
    g.bind('schema', SCHEMA)

    # Load Graph
    g.parse(OUT_GRAPH, format="nt")

    # Selected queries
    queries = QUERIES[:3]

    print("Number of querys selected:", len(queries))

    # Write Results
    for q in queries:
        dump2csv(OUT_QUERY + str(q.id), make_query(q))

    # Write queries
    with open(QUERYS_SPARQL, "w") as f:
        for q in queries:
            f.write(f"# Query {q.id}: {q.description}:\n")
            f.write(q.query + "\n\n")

    print("Finish")
