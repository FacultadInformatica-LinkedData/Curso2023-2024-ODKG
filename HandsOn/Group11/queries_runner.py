import rdflib
import time


DATA_FILE_PATH = "./rdf/dataset-with-links-updated.ttl" 


t_start = time.perf_counter()
graph = rdflib.Graph()
print(f"Graph init time: {time.perf_counter() - t_start}s")


t_start = time.perf_counter()
result = graph.parse(DATA_FILE_PATH, format='ttl')
print(f"Graph loading time: {time.perf_counter() - t_start}s")

query = """
PREFIX art: <http://artwork.org/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX own: <https://soum2111.github.io/>

SELECT ?artist ?title ?link
WHERE {
  ?artwork a sch:VisualArtwork .
  ?artwork own:hasAccessionNumber "A00001" .
  ?artwork sch:artist ?artist .
  ?artwork sch:name ?title .
  ?artist owl:sameAs ?link .
}"""

t_start = time.perf_counter()
results = graph.query(query)
print(f"Query time: {time.perf_counter() - t_start}s")

for row in results:
    print(row)
