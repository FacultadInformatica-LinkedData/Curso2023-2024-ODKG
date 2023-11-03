import rdflib


DATA_FILE_PATH = "./rdf/dataset.ttl" 


graph = rdflib.Graph()

result = graph.parse(DATA_FILE_PATH, format='ttl')
query = """
PREFIX art: <http://artwork.org/>

SELECT (COUNT(DISTINCT ?id) as ?distinctIdCount)
WHERE {
  ?artwork a art:Artwork .
  ?artwork art:hasId ?id .
}"""

results = graph.query(query)
for row in results:
    distinct_id_count = row.distinctIdCount
    print(f"Distinct ID Count: {distinct_id_count}")
