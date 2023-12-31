# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ujMF6_YdBqkGR-in-31DxiGWYCja3npp

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0/"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

ns = Namespace("http://somewhere#")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

#Sparql
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
    SELECT ?subClass
    WHERE {
        ?subClass rdfs:subClassOf+ ns:LivingThing.
    }
''',
initNs={"rdfs": RDFS, "ns": ns}
)

# Visualize the results
for r in g.query(q1):
  print(r.subClass)

#RDFLib
from rdflib import Graph, Namespace, RDF, RDFS

def get_all_subclasses7_1(graph, namespace, superclass_uri, seen=None):
    if seen is None:
        seen = set()

    results = set()

    for subj, _, obj in graph.triples((None, RDFS.subClassOf, superclass_uri)):
      if subj not in seen:
          seen.add(subj)
          results.add(subj)
          results.update(get_all_subclasses7_1(graph, namespace, subj, seen))

    return results

living_thing_uri = ns.LivingThing
results = get_all_subclasses7_1(g,ns,living_thing_uri)
for item in results:
  print(item)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

#Sparql
q2 = prepareQuery('''
    SELECT ?person
    WHERE {
        {
        ?person rdf:type ns:Person.
        }
        UNION {
            ?tipo rdfs:subClassOf+ ns:Person.
            ?person rdf:type ?tipo.
            }
    }
''',
initNs={"rdfs": RDFS, "ns": ns, "rdf": RDF}
)

# Visualize the results
for r in g.query(q2):
  print(r.person)

#RDFLib
results = set()
def get_all_7_2(superclass_uri):
  for subj, p, obj in g.triples((None, RDFS.subClassOf, superclass_uri)):
    results.add(subj)
    get_all_7_2(subj)
  return results

person_uri = ns.Person
results = get_all_7_2(person_uri)
results.add(person_uri)
results2 = set()
for item in results:
  for subj, p, obj in g.triples((None, RDF.type, item)):
    results2.add(subj)
for items in results2:
  print(items)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

#Sparql
q3 = prepareQuery('''
    SELECT ?person ?prop ?obj
    WHERE { {
        ?person rdf:type ns:Animal.
        }
        UNION {
        ?person rdf:type ns:Person.
        }
        ?person ?prop ?obj
        }
''',
initNs={"rdfs": RDFS, "ns": ns,"rdf": RDF}
)

# Visualize the results
for r in g.query(q3):
  print(r.person,r.prop,r.obj)

#RDFLib
def get_all_7_3(graph,namespace_person, namespace_animal):
  results = []
  for s1, p1, o1 in graph:
    for s2, p2, o2 in graph.triples((s1, RDF.type, None)):
      if o2 == namespace_person or o2 == namespace_animal:
        results.append((str(s1), str(p1), str(o1)))
  return results

results = get_all_7_3(g,ns.Person, ns.Animal)
# Visualize the results
for (s,p,o) in results:
  print(s,p,o)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

#Sparql
from rdflib import FOAF
from rdflib import XSD
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q4 = prepareQuery('''
    SELECT ?person
    WHERE {
        ?person foaf:knows ?RockySmith.
        ?RockySmith vcard:Given ?RockySmithFullName.
    }
''',
initNs={"foaf": FOAF,"vcard": VCARD, "xsd":XSD}
)

# Visualize the results
for r in g.query(q4,initBindings = {'?RockySmithFullName' : Literal('Rocky', datatype=XSD.string)}):
  print(r.person)

#RDFLib
def get_all_7_4(graph,namespace):
  results = set()
  for s, p, o in graph.triples((None, RDF.type, namespace)):
    for s2, p2, o2 in graph.triples((s, FOAF.knows, ns.RockySmith)):
        results.add(s2)
  for s, p, o in graph.triples((None, RDFS.subClassOf, namespace)):
    for s2, p2, o2 in graph.triples((None, None, s)):
      for s3, p3, o3 in graph.triples((s2, FOAF.knows, ns.RockySmith)):
        results.add(s3)
  return results

results = get_all_7_4(g,ns.Person)
for items in results:
  for _, _, name in g.triples((items, VCARD.Given, None)):
    print(name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

#Sparql
q5 = prepareQuery('''
    SELECT DISTINCT ?person
    WHERE {
        ?person foaf:knows ?someone .
        FILTER (?person != ?someone).
    }
    GROUP BY ?person
    HAVING (COUNT(?someone) >= 2)
''',
initNs={"foaf": FOAF}
)

# Visualize the results
for r in g.query(q5):
  print(r.person)

#RDFlib
def get_all_7_5(graph):
  entities_dictionary = {}
  results = []
  for s, p, o in g.triples((None, FOAF.knows, None)):
    if s != o:
      if s in entities_dictionary:
        entities_dictionary[s] += 1
      else:
        entities_dictionary[s] = 1
  for key,name in entities_dictionary.items():
    if key >= 2:
      results.append(key)
  return results

results = get_all_7_5(g)
for item in results:
  print(item)