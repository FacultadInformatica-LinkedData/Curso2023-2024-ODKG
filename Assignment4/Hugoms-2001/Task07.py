#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Task 07: Querying RDF(s)


# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# In[2]:


#First let's read the RDF file
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# In[28]:


#TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

print("SPARQL:")
q1 = prepareQuery('''
  SELECT ?SubClass WHERE { 
    ?SubClass rdfs:subClassOf* ns:LivingThing.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)
for r in g.query(q1):
  print(r)

print("RDFLib:")

def subclasses(subclass):
    print(subclass)
    for subclass, _, _ in g.triples((None, RDFS.subClassOf, subclass)):
        subclasses(subclass)

subclasses(ns.LivingThing)


# In[29]:


#TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)

print("SPARQL:")
q2 = prepareQuery('''
  SELECT ?instance WHERE { 
    ?instance a ?type.
    ?type rdfs:subClassOf* ns:Person
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)
for r in g.query(q2):
  print(r)

print("RDFLib:")
def individuals(Class):
    for individual, _, _ in g.triples((None, RDF.type, Class)):
        print(individual)

    for subclass, _, _ in g.triples((None, RDFS.subClassOf, Class)):
        individuals(subclass)
individuals(ns.Person)


# In[30]:


#TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. 
#You do not need to list the individuals of the subclasses of person

print("SPARQL:")
q3 = prepareQuery('''
    SELECT ?individual ?p ?o WHERE {
    { 
    ?individual rdf:type ns:Person.
    }
    UNION
    {
    ?individual rdf:type ns:Animal.
    }
    ?individual ?p ?o
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)
for r in g.query(q3):
  print(r)

print("RDFLib:")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    for s0, p0, o0 in g.triples((s, None, None)):
      print(p0, o0)

for s, p, o in g.triples((None, RDF.type, ns.Animal)):
    for s0, p0, o0 in g.triples((s, None, None)):
      print(p0, o0)


# In[31]:


#TASK 7.4: List the name of the persons who know Rocky
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

q4 = prepareQuery('''
    SELECT ?name
    WHERE {
    ?person foaf:knows ns:RockySmith .
    ?person vcard:FN ?name .
  }  
  ''',
  initNs = {"rdf": RDF, "ns": ns, "rdfs": RDFS, "vcard":vcard}
)

for row in g.query(q4):
  print(row.name)

print("RDFLib:")
def find_persons(individual):
    persons = []
    for person in g.subjects(predicate=foaf.knows, object=ns.RockySmith):
        persons.append(person)
    return persons

persons = find_persons(ns.RockySmith)

for person in persons:
    name = g.value(subject=person, predicate=vcard.FN)
    if name:
        print(name)


# In[33]:


#Task 7.5: List the entities who know at least two other entities in the graph

q5 = prepareQuery('''
    SELECT ?entity
    WHERE {
        ?entity foaf:knows ?known1, ?known2.
        FILTER (?known1 != ?known2)
    }  
  ''',
  initNs={"foaf": FOAF}
)

unique_entities = set()

for result in g.query(q5):
    unique_entities.add(result.entity)

for entity in unique_entities:
    print(entity)
    
    
print("RDFLib:")
def find_entities():
    entities = set()
    for entity in g.subjects(predicate=foaf.knows):
        known_entities = set(g.objects(subject=entity, predicate=foaf.knows))
        if len(known_entities) >= 2:
            entities.add(entity)
    return entities

entities = find_entities()

for entity in entities:
    print(entity)

