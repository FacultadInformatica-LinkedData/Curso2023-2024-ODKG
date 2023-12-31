# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lv2-pNkfm7CwgMKQwy0NXzu33Yv9qkTh

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

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF

ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

print("SPARQL VERSION:")

q1 = prepareQuery('''
  SELECT ?subclass
  WHERE {
    ?subclass rdfs:subClassOf/rdfs:subClassOf* ns:LivingThing .
}
  ''',
  initNs = {"ns": ns, "rdfs": RDFS}
)

for r in g.query(q1):
  print(r.subclass)

print("\nRDFLib VERSION:")

subclasses = []
def list_subclasses(target):
    for s,p,o in g.triples((None, RDFS.subClassOf, target)):
        subclasses.append(s)
        list_subclasses(s)

list_subclasses(ns.LivingThing)
for s in subclasses:
    print(s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# SPARQL VERSION
print("SPARQL VERSION:")
q2 = prepareQuery('''
  SELECT ?individuals WHERE {
    ?subclasses rdfs:subClassOf* ns:Person.
    ?individuals a ?subclasses.
  }
''',
  initNs = {"ns": ns, "rdfs": RDFS}
)

for r in g.query(q2):
    print(r.individuals)

# RDFLib VERSION
print("\nRDFLib VERSION:")

for t,p,o in g.triples((None, RDF.type, ns.Person)):
  print(t)

for t,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for a,b,c in g.triples((None, RDF.type, t)):
    print(a)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# SPARQL VERSION
print("SPARQL VERSION:")
q3 = prepareQuery('''
SELECT ?individual ?property ?value
WHERE {
    {
        ?individual rdf:type ns:Person .
        ?individual ?property ?value .
    } UNION {
        ?individual rdf:type ns:Animal .
        ?individual ?property ?value .
    }
}
''',
  initNs = {"ns": ns, "rdfs": RDFS}
)

for r in g.query(q3):
    print(f"Individual: {r.individual}, Property: {r.property}, Value: {r.value}")

# RDFLib VERSION
print("\nRDFLib VERSION:")

individuals = set()
properties = set()

for s, o in g.subject_objects(RDF.type):
    if o == ns.Person or o == ns.Animal:
        individuals.add(s)
        for p, v in g.predicate_objects(s):
            properties.add((s, p, v))

for i, p, v in properties:
    print(f"Individual: {i}, Property: {p}, Value: {v}")

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# SPARQL VERSION
print("SPARQL VERSION:")
q4 = prepareQuery('''
  SELECT ?name WHERE {
    ?person <http://xmlns.com/foaf/0.1/knows> <http://somewhere#RockySmith>.
    ?person <http://www.w3.org/2001/vcard-rdf/3.0/FN> ?name.
  }
''',
  initNs = {"ns": ns, "rdfs": RDFS}
)

print(f"Person who knows Rocky:")
for r in g.query(q4):
    print(r.name)

# RDFLib Version
print("\nRDFLib VERSION:")
print(f"Person who knows Rocky:")
persons = []
def list_persons(target):
    for s,p,o in g.triples((None, RDF.type, target)):
        persons.append(s)
    for s,p,o in g.triples((None, RDFS.subClassOf, target)):
        list_persons(s)
list_persons(ns.Person)

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
knowers = []
for count in persons:
    for s, p, o in g.triples((count, FOAF.knows, ns.RockySmith)):
        knowers.append(count)
for k in knowers:
    for s, p, o in g.triples((k, vcard.FN, None)):
        knowers[knowers.index(k)] = o

for k in knowers:
    print(k)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# SPARQL VERSION
print("SPARQL VERSION:")
q5 = prepareQuery('''
SELECT ?entity
WHERE {
    ?entity foaf:knows ?known1 .
    ?entity foaf:knows ?known2 .
    FILTER(?known1 != ?known2)
}
GROUP BY ?entity
HAVING (COUNT(?entity) >= 2)
''')

print(f"Entity who knows at least two others:")
for r in g.query(q5):
    print(r.entity)

# RDFLib Version
print("\nRDFLib VERSION:")

knowledge_dict = {}

for s, o in g.subject_objects(FOAF.knows):
    if s not in knowledge_dict:
        knowledge_dict[s] = set()
    knowledge_dict[s].add(o)

entities_with_multiple_known = [entity for entity, known in knowledge_dict.items() if len(known) >= 2]

print(f"Entity who knows at least two others:")
for entity in entities_with_multiple_known:
     print(entity)