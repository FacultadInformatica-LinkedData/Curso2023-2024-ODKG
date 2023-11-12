from rdflib import Graph, Namespace

g = Graph()
g.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")

print("\nSPARQL:")
query = '''
  SELECT DISTINCT ?district
  WHERE {
    ?address a ns:Address ;
           ns:belongsTo ?district ;
  }
'''
# Almacena los resultados en una lista
prices_list = [row.district for row in g.query(query, initNs={"ns": ns, "schema": schema})]

# Visualiza los resultados
print("Precios:", prices_list)


# for s, p, o in g:
#   print(s,p,o)