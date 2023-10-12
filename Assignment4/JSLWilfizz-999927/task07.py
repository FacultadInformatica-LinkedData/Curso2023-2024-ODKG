# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a-xqsJzK0Oa1Z93ecEoYWyoKPQtan8YF

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
# Visualize the results

ns = Namespace("http://somewhere#")
#With SPARQL
q1 = prepareQuery('''
  SELECT  ?sub  WHERE {
    ?sub rdfs:subClassOf ns:LivingThing.
  }
  ''', initNs={"ns": ns}
                  )
for r in g.query(q1):
    print(r.sub)
print("--------------------------------")
#With RDFlib

for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    print(s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# Visualize the results

ns = Namespace("http://somewhere#")
#With SPARQL

q1 = prepareQuery('''
  SELECT  ?persona  WHERE {
    ?persona rdf:type ns:Person
  }
  ''', initNs={"ns": ns}
                  )
for r in g.query(q1):
    print(r.persona)

q2 = prepareQuery('''
  SELECT  ?person WHERE {
    ?sub rdfs:subClassOf ns:Person.
    ?person a ?sub.
  }
  ''', initNs={"ns": ns}
                  )
for r in g.query(q2):
    print(r.person)


print("--------------------------------")
#With RDFlib

for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
        print(s1)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO

#With SPARQL
q1 = prepareQuery('''
  SELECT ?instance ?predicate ?object
  WHERE {
      ?sub rdfs:subClassOf* ns:LivingThing.
      ?instance a ?sub.
      ?instance ?predicate ?object.
  }
  ''', initNs={"ns": ns}
                  )
for r in g.query(q1):
    print(r.instance,r.predicate,r.object)
# Visualize the results


print("--------------------------------")
#With RDFlib


for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    for s1, p1, o1 in g.triples((None, None, s)):
      print(s1)
      for s2, p2, o2 in g.triples((s1, None, None)):
       print(s2,p2,o2)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD= Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")


# Visualize the results
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
  for s1, p1, o1 in g.triples((s, VCARD.FN, None)):
      print(f"{o1} know Rocky")

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
from collections import defaultdict


dicc = defaultdict(int)

for name, p, o in g.triples((None, FOAF.knows, None)):
  dicc[name] += 1
for name in dicc.keys():
  if dicc[name] >= 2:
    for s, p, o in g.triples((name, VCARD.FN, None)):
        print(f"{o} know {dicc[name]} entities")
# Visualize the results

