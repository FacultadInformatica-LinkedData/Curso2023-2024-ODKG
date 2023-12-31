# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
  https://colab.research.google.com/drive/1hSngd1VeIv2Z9WkQU6apsnESwwlnynsX

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal, FOAF
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

NS = Namespace("http://somewhere#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# With SPARQL
q1 = prepareQuery('''
  SELECT ?subclass
  WHERE
  {
    ?subclass rdfs:subClassOf/rdfs:subClassOf* ns:LivingThing.
  }
  ''',
  initNs = { "rdfs":RDFS, "ns":NS}
)

print("SPARQL")
for r in g.query(q1):
  print(r.subclass)

# With RDFlib
subclasses = set()
classes = [NS.LivingThing]

for subclass in classes:
  for s, p, o in g.triples((None, RDFS.subClassOf, subclass)):
    subclasses.add(s)
    classes.append(s)

print("RDFlib")
for subclass in subclasses:
  print(subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# With SPARQL
q2 = prepareQuery('''
  SELECT ?individual
  WHERE
  {
    ?individual rdf:type/rdfs:subClassOf* ns:Person.
  }
  ''',
  initNs={"rdf": RDF,"rdfs": RDFS, "ns": NS}
)

print("SPARQL")
for r in g.query(q2):
  print(r.individual)

# With RDFlib
individuals = set()

for s, p, o in g.triples((None, RDF.type, None)):
  for subclass in g.transitive_objects(subject=o, predicate=RDFS.subClassOf):
    if subclass == NS.Person:
      individuals.add(s)

print("RDFlib")
for individual in individuals:
  print(individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# With SPARQL
q3 = prepareQuery('''
  SELECT ?individual ?Property ?Value ?Class
  WHERE
  {
    ?individual rdf:type ?Class.
    ?individual ?Property ?Value
    FILTER(?Class = ns:Person || ?Class = ns:Animal)
  }
  ''',
  initNs={"rdf": RDF, "ns": NS}
)

print("SPARQL")
for r in g.query(q3):
    print(r.individual, r.Class, r.Property, r.Value)

# With RDFlib
print("RDFlib")
for s, p, o in g.triples((None, RDF.type, None)):
  for class_type in g.objects(subject=s, predicate=RDF.type):
    if class_type == NS.Person or class_type == NS.Animal:
      for prop, value in g.predicate_objects(subject=s):
        print(s,class_type,prop,value)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# With SPARQL
q4 = prepareQuery('''
  SELECT DISTINCT ?personName
  WHERE
  {
    ?person ns:knows ?rocky .
    ?person foaf:name ?personName .
    ?rocky foaf:name "Rocky" .
  }
  ''',
  initNs = { 'ns': NS, 'foaf': FOAF }
)

print("SPARQL")
for r in g.query(q4):
    print(r.personName)

# With RDFlib
knows_rocky = set()
for s, p, o in g.triples((None, NS.knows, None)):
  for s2, p2, o2 in g.triples((s, FOAF.name, 'Rocky')):
    knows_rocky.add(s)


print("RDFlib")
for person in knows_rocky:
  for s, _, name in g.triples((person, FOAF.name, None)):
    print(name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# With SPARQL
q5= prepareQuery('''
  SELECT ?entity  WHERE
  {
    ?entity foaf:knows ?persons.
    FILTER(?entity != ?persons).
  }
  GROUP BY ?entity
  HAVING (COUNT(DISTINCT ?persons) >= 2)
  ''',
  initNs = {"foaf":FOAF}
)

print("SPARQL")
for r in g.query(q5):
  print(r.entity)

# With RDFlib
entities = {}
for s, p, o in g.triples((None, FOAF.knows, None)):
  if s in entities:
    entities[s].add(o) 
  else:
    entities[s] = {o}  

selected_entities = [entity for entity, persons in entities.items() if len(persons) > 1]

print("RDFlib")
for r in selected_entities:
  print(r)