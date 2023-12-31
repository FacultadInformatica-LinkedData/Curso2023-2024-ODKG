# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RordfVihjdrEiOACdFs1kZ6W0X8FZ_8O

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

for s, p, o in g:
  print(s,p,o)

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
# Visualize the results
################################################################
print("RDF:")
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")

for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)
################################################################
print("SPARQL:")
q1 = prepareQuery('''
  SELECT ?subClass WHERE {
    ?subClass rdfs:subClassOf* ns:LivingThing.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)

for r in g.query(q1):
  print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# Visualize the results

ns = Namespace("http://somewhere#")

################################################################
print("RDF:")

for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for ss,pp,oo in g.triples((None, RDF.type, s)):
      print(ss)
################################################################
print("SPARQL:")

q2 = prepareQuery('''
  SELECT ?individual WHERE {
    { ?individual rdf:type ns:Person
    }
    UNION
    { ?individual rdf:type ?Class.
    ?Class rdfs:subClassOf* ns:Person.
    }
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf":RDF, "ns": ns}
)

for r in g.query(q2):
  print(r.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
# Visualize the results

ns = Namespace("http://somewhere#")

################################################################
print("RDF:")

for s,p,o in g.triples((None, RDF.type, ns.Person)):
  for ss,pp,oo in g.triples((s, None, None)):
    print(s, pp)

for s,p,o in g.triples((None, RDF.type, ns.Animal)):
  for ss,pp,oo in g.triples((s, None, None)):
    print(s, pp)
################################################################
print("SPARQL:")
q3 = prepareQuery('''
  SELECT ?individual ?properties ?property WHERE { {
    ?individual rdf:type ns:Person.
    ?individual ?properties ?property
    }
    UNION {
    ?individual rdf:type ns:Animal.
    ?individual ?properties ?property
    }
  }
  ''',
  initNs = { "rdfs": RDFS, "rdf":RDF, "ns": ns}
)

for r in g.query(q3):
  print(r.individual, r.properties)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
# Visualize the results
from rdflib import FOAF
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

################################################################
print("RDF")
for s,p,o in g.triples((None, FOAF.knows, ns.RockySmith)):
  print(s)

################################################################
print("SPARQL")
q4 = prepareQuery('''
  SELECT DISTINCT ?person ?name
    WHERE {
        ?person foaf:knows ns:RockySmith.
        ?person vcard:Given ?name
    }
  ''',
  initNs = { "rdfs": RDFS, "rdf":RDF, "ns": ns, "foaf":FOAF, "vcard": VCARD}
)

for r in g.query(q4):
  print(r.person)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
# Visualize the results
from rdflib import FOAF
ns = Namespace("http://somewhere#")

################################################################
print("RDF")
people = []
count = 0
for s,p,o in g.triples((None, FOAF.knows, None)):
  for ss,pp,oo in g.triples((s,FOAF.knows,None)):
    count = count + 1
    if count >= 2:
      count = 0
      if ss not in people:
        people.append(ss)

print(people)

################################################################
print("RDF")

q5 = prepareQuery('''
  SELECT ?person (COUNT(?someone) as ?counter) WHERE{
    ?person foaf:knows ?someone.
  }
  GROUP BY ?person
  HAVING (COUNT(?someone) >= 2)
  ''',
  initNs = { "rdfs": RDFS, "rdf":RDF, "ns": ns, "foaf":FOAF}
)

for r in g.query(q5):
  print(r.person)