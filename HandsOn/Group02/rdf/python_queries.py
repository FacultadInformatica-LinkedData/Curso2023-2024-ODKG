#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery
g = Graph()

print('Parse rdf')

g.parse("rdf_with_rules.ttl", format="ttl")

'''print('Print rdf')
print(g.serialize(format="ttl"))'''

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#>")
madridonc = Namespace("http://madridalfresco.es/lcc/ontology/locales#")
madridrec = Namespace ("http://madridalfresco.es/lcc/resource/")

print("Q1")
q1 = prepareQuery('''
    SELECT (count(?Terraza) as ?o) 
    WHERE { 
        ?Terraza a madridonc:Terraza;
            madridonc:sillas ?sillas;
        FILTER(?sillas>=10).
    }
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q1):
  print(r)
  
print("Q2")
q2 = prepareQuery('''
    SELECT (?Distrito as ?o)
    WHERE {
    ?Distrito rdf:type madridonc:Distrito;
                madridonc:tipoVia ?via;
    FILTER(?via!="AVENIDA"). 
    } LIMIT 5
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q2):
  print(r)
  
print("Q3")
q3 = prepareQuery('''
    SELECT DISTINCT ?obj ?ndir 
    WHERE {
        ?loc rdf:type madridonc:Local ;
            madridonc:rotulo ?obj ;
            madridonc:perteneceADistrito ?dist .
        ?dist madridonc:nombreDistrito ?ndir
        FILTER(?ndir = "SALAMANCA")
    }
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q3):
  print(r)
  
print("Q4")
q4 = prepareQuery('''
    SELECT DISTINCT ?obj ?ndir 
    WHERE {
      ?loc rdf:type madridonc:Local ;
      madridonc:rotulo ?obj ;
      madridonc:perteneceADistrito ?dist .
      ?dist madridonc:nombreCalle ?ndir.
    } LIMIT 4
  ''',
  initNs = { "madridonc": madridonc}
)
for r in g.query(q4):
  print(r)