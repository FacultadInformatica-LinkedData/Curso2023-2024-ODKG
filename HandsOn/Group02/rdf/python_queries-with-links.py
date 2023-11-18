#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery
g = Graph()

print('Parse rdf')

g.parse("rdf_with_rules-with-links.ttl", format="ttl")

'''print('Print rdf')
print(g.serialize(format="ttl"))'''

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#>")
madridonc = Namespace("http://madridalfresco.es/lcc/ontology/locales#")
madridrec = Namespace ("http://madridalfresco.es/lcc/resource/")

print("Q1")
q1 = prepareQuery('''
    SELECT DISTINCT ?dist ?samedist 
    WHERE { 
        ?dist madridonc:sameAsNombreDistrito ?samedist.
    } LIMIT 10
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q1):
  print(r)
  
print("Q2")
q2 = prepareQuery('''
    SELECT DISTINCT ?barrio ?samebarrio 
    WHERE { 
        ?barrio madridonc:sameAsBarrio ?samebarrio.
    } LIMIT 10
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q2):
  print(r)
  
print("Q3")
q3 = prepareQuery('''
    SELECT DISTINCT ?tipoVia ?sametipoVia 
    WHERE { 
        ?tipoVia madridonc:sameAsTipoVia ?sametipoVia.
    } LIMIT 10
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q3):
  print(r)
  
