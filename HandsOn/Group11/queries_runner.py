import rdflib
import time


DATA_FILE_PATH = "./rdf/dataset.ttl" 


t_start = time.perf_counter()
graph = rdflib.Graph()
print(f"Graph init time: {time.perf_counter() - t_start}s")


t_start = time.perf_counter()
result = graph.parse(DATA_FILE_PATH, format='ttl')
print(f"Graph loading time: {time.perf_counter() - t_start}s")

query = """
PREFIX art: <http://artwork.org/>

SELECT (COUNT(DISTINCT ?id) as ?distinctIdCount)
WHERE {
  ?artwork a art:Artwork .
  ?artwork art:hasId ?id .
}"""

t_start = time.perf_counter()
results = graph.query(query)
print(f"Query time: {time.perf_counter() - t_start}s")

for row in results:
    print(row)
