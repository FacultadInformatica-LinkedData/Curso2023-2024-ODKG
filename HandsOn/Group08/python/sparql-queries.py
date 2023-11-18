from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph
from rdflib.query import Result

from globals import OUT_GRAPH, OUT_GRAPH_LINKS, OUT_QUERY, QUERYS_SPARQL, QUERYS_SPARQL_LINKS
from pydantic import BaseModel

from time import time

PREFIX = """

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <https://dbpedia.org/ontology/>
PREFIX ns: <http://www.semanticweb.org/upm/opendata/group08/ontology/UniversityInformation#>
PREFIX schema: <https://schema.org/> 

"""


class Query(BaseModel):
    id: int
    description: str
    query: str


QUERIES = [
    Query(id=1, description="""Select all the possible values of the property
          # dbo:city of the entities that belong to class n:University """,
          query="""
            SELECT DISTINCT ?nameCity ?uniname WHERE {
                ?university dbo:city ?city .
                ?city rdf:label ?nameCity.
                ?university rdf:type ns:University.
                ?university rdf:label ?uniname. 
        }    
    """),
    Query(id=2, description="""Select all the scores and years of all the Liberal Arts Colleges Rankings
          # for all the Universities located in the state of Florida)""",
          query="""
                SELECT ?uniname ?score ?year ?stateName WHERE {
                    ?university rdf:type ns:University.
  					?university rdf:label ?uniname. 
                    ?ranking ns:score ?score.
                    ?ranking ns:yearPublished ?year.
                    ?university ns:hasRanking  ?ranking .
                    ?ranking rdf:type ns:UniversityRankingLiberalArts.
                    ?university dbo:state ?state.
  					?state rdf:label ?stateName.
  
  				  FILTER (xsd:string(?stateName) = "Florida"^^xsd:string)
                } 
        """),
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
                SELECT DISTINCT ?uniname ?longitude ?latitude ?score WHERE {
                    ?university rdf:type ns:University.
                    ?university rdf:label ?uniname. 
                    ?university ns:hasRanking ?ranking .
  					?ranking rdf:type ns:RankingUSNews.
  					?ranking ns:score ?score.
                    ?university schema:longitude ?longitude.
                    ?university schema:latitude ?latitude.
                    
  					FILTER (xsd:string(?score) = "1"^^xsd:string)
                }    
                """,
          )]

QUERIES_LINKS = [

    Query(id=5, description="Retrieve the city and state of wikidata of university",
          query="""    
                SELECT ?nameCity ?uriCityWikiData ?nameState ?uriStateWikiData WHERE {
                    ?university dbo:city ?city .
                    ?city rdf:label ?nameCity.
                    ?city owl:sameAs ?uriCityWikiData.
                    ?university dbo:state ?state.
                    ?state rdf:label ?nameState.
                    ?state owl:sameAs ?uriStateWikiData.
                    ?university rdf:type ns:University.
                }    
                """
          )
]


def dump2csv(filename: str, result: Result):
    with open(filename+"-result.csv", "wb") as f:
        f.write(result.serialize(format="csv"))


def make_query(g: Graph, query: Query, limit: int = 50):

    limit = "\nLIMIT " + str(limit)

    result = g.query(prepareQuery(PREFIX + query.query + limit))
    return result


def write_querys(path: str, queries: list[Query]):

    with open(path, "w") as f:
        f.write("# University Infomation Ontology Queries\n\n")
        f.write("# Prefixs:\n" + PREFIX + "\n\n")

        for q in queries:
            f.write(f"# Query {q.id}: {q.description}:\n")
            f.write(q.query + "\n\n")


def consult_query(g: Graph, queries: list[Query]):

    for q in queries:
        print("-"*40)
        print("Consulting:", q.id)

        start = time()
        result = make_query(g, q)
        end = time()

        print("Number of results", len(result))
        print(f"Time Query {q.id}:  {round(end-start, 3)} s")
        print("Writting query:", q.id, flush=True)
        dump2csv(OUT_QUERY + str(q.id), result)
        print("Writted", flush=True)


def test_graph(path_g: str, format: str, path_q: str, queries: list[Query]):
    g = Graph()

    print("Testing Graph")

    print("Number of querys selected:", len(queries))

    write_querys(path_q, queries)

    print("Queries writted")

    # Load Graph
    g.parse(path_g, format=format)

    print("Load Graph", path_g)

    consult_query(g, queries)

    print("Result writted")

    print("Finish")


if __name__ == "__main__":

    test_graph(OUT_GRAPH_LINKS, OUT_GRAPH_LINKS.split(
        ".")[-1], QUERYS_SPARQL_LINKS, QUERIES_LINKS)

    print("\n"*2, "-"*20, "\n"*2)

    test_graph(OUT_GRAPH, OUT_GRAPH.split(".")[-1], QUERYS_SPARQL, QUERIES)
