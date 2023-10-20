from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib import Graph, Namespace, Literal, XSD
import morph_kgc
import pandas as pd

# %% Eliminar duplicados
path = "HandsOn/Group08/csv2/us-colleges-and-universities.csv"

csv = pd.read_csv(path)

duplicados = csv['IPEDSID'].duplicated(keep=False)
print("Number of dups", len(csv[duplicados]))

print("Old:", len(csv))

csv = csv.drop_duplicates(subset="IPEDSID", keep="last")


print("New:", len(csv))
print(csv.keys())

# %% Poner los valores de las columnas en un formato adecuado para poder realizar el mapping


columna = csv['NAME']
columna2 = csv['CITY']


columna = columna.str.title()
columna2 = columna2.str.title()
columna4 = 'United States'

csv['NAME'] = columna
csv['CITY'] = columna2
csv['COUNTRY'] = columna4


csv.to_csv(
    'HandsOn/Group08/csv2/us-colleges-and-universities-modified.csv', index=False)


# %% Crear grafo en formato RDF
print(RDF)

config = """
    [CONFIGURATION]
    output_file= HandsOn/Group08/rdf/us-colleges-and-universities.ttl
    [DataSource1]
    mappings= HandsOn/Group08/mappings/us-colleges-and-universities/us-colleges-and-universities.ttl
         """
g = morph_kgc.materialize(config)


# %% Crear consulta SPARQL
g.namespace_manager.bind('ns', Namespace(
    "http://www.semanticweb.org/upm/opendata/group08/ontologies/ns#"), override=False)
g.namespace_manager.bind('schema', Namespace(
    "https://schema.org/"), override=False)

ns = Namespace(
    'http://www.semanticweb.org/upm/opendata/group08/ontologies/ns#')
schema = Namespace("https://schema.org/")
dbo = Namespace("https://dbpedia.org/ontology/")
dbp = Namespace("https://dbpedia.org/page/")

# Binding the prefixes
g.bind('rdfs', RDFS)
g.bind('ns', ns)
g.bind('foaf', FOAF)
g.bind('rdf', RDF)
g.bind('dbo', dbo)
g.bind('dbp', dbp)
g.bind('schema', schema)


# Define the SPARQL query: Select all the possible values of the property dbo:city of the entities that belong to class n:University
query_text = """    
    SELECT ?value WHERE {
        ?individual dbo:city ?value .
        ?individual rdf:type ns:University.
    }    
"""
# Prepare the query
query = prepareQuery(query_text, initNs={"ns": ns, "dbo": dbo, "rdf": RDF})

# Execute the query
# Visualize the results
for row in g.query(query):
    print(f'City: {row}')
