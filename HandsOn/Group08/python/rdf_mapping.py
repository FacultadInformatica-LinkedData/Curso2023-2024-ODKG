from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib import Graph, Namespace, Literal, XSD
import morph_kgc
import pandas as pd

# %% Eliminar duplicados

PATH = "csv2/us-colleges-and-universities.csv"

csv = pd.read_csv(PATH)

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


csv.to_csv('csv2/us-colleges-and-universities-modified.csv', index=False)

# %% Preprocesado sergio
data = pd.read_csv(
    "csv2/US-News-Rankings-Liberal-Arts-Colleges-Through-2023-updated.csv")
data = data.melt(id_vars=['IPEDSID'], var_name='Year', value_name='Ranking')
data.to_csv(
    'csv2/US-News-Rankings-Liberal-Arts-Colleges-Through-2023-updated-2.csv', index=False)

# %% Preprocesado adri
data_2 = pd.read_csv(
    "csv2/US-News-Rankings-Universities-Through-2023-updated.csv")
data_2 = data_2.melt(id_vars=['IPEDSID'],
                     var_name='Year', value_name='Ranking')
data_2.to_csv(
    'csv2/US-News-Rankings-Universities-Through-2023-updated2.csv', index=False)

# %% Crear grafo en formato RDF
print(RDF)

config = """
    [CONFIGURATION]
    output_file= rdf/Universities.ttl
    [DataSource1]
    mappings= mappings/UniversityMapping.ttl
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

print("\n\n", "-"*40, "\n\n")

# %% Query 2 : Select all the values and years of all the Liberal Arts Colleges
query_text2 = """    
    SELECT ?value ?year WHERE {
        ?ranking ns:score ?value.
        ?ranking ns:yearPublished ?year.
        ?individual ns:hasLiberalArtsRanking  ?ranking .
        ?individual rdf:type ns:University.
    }    
"""


# Prepare the query
query = prepareQuery(query_text2, initNs={"ns": ns, "dbo": dbo, "rdf": RDF})

# Execute the query
# Visualize the results
for row in g.query(query):
    print(f'Value: {row[0]} Year; {row[1]}')

print("\n\n", "-"*40, "\n\n")

# %% Query 3: Select the values of admission rate of all the entities of type University

query_text3 = """    
    SELECT ?value WHERE {
        ?individual rdf:type ns:University.
        ?individual ns:hasAdmisionRate ?rate .
        ?rate ns:value ?value
    }    
"""
# Prepare the query
query = prepareQuery(query_text3, initNs={"ns": ns, "rdf": RDF})

# Execute the query
# Visualize the results
for row in g.query(query):
    print(f'Rate: {row}')

print("\n\n", "-"*40, "\n\n")
