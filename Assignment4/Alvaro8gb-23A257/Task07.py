#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


from collections import Counter
from rdflib.plugins.sparql import prepareQuery
from typing import List
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS
from rdflib import Graph, Namespace
get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[2]:


g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace(
    "http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/rdf/example6.rdf", format="xml")


# In[3]:


NS = Namespace("http://somewhere#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


def get_subclasses(class_uri: URIRef, subclasses: List[URIRef], graph: Graph, visited: set = None) -> List[URIRef]:
    """
    Recursively retrieves all subclasses of a given class in an RDF graph.

    :param class_uri: The URI of the class to find subclasses for.
    :param subclasses: A list to accumulate the subclasses.
    :param graph: The RDF graph to search within.
    :param visited: A set to keep track of visited URIs to prevent infinite loops.
    :return: A list of subclass URIs.
    """
    if visited is None:
        visited = set()

    for s, _, _ in graph.triples((None, RDFS.subClassOf, class_uri)):
        if s not in visited:
            visited.add(s)
            subclasses.append(s)
            get_subclasses(s, subclasses, graph, visited)

    return subclasses

# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[4]:


print("RDFlib:")

visited = set()
subs = get_subclasses(NS.LivingThing, subclasses=[NS.LivingThing], graph=g, visited=visited)

for s in subs:
    print(s)

print("SPARQL:")
q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject rdfs:subClassOf* ns:LivingThing.
  }
  ''',
                  initNs={"rdfs": RDFS, "ns": NS}
                  )
for r in g.query(q1):
    print(r.Subject)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
#

# In[5]:


print("RDFlib:")

visited = set()
for s in get_subclasses(NS.Person, subclasses=[NS.Person], graph=g, visited=visited):
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
        print(s1)



print("SPARQL:")

q2 = prepareQuery('''
  SELECT ?Individual WHERE {
    ?Subject rdfs:subClassOf* ns:Person.
    ?Individual rdf:type ?Subject
  }
  ''',
                  initNs={"rdfs": RDFS, "ns": NS, "rdf": RDF}
                  )

for r in g.query(q2):
    print(r.Individual)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
#

# In[6]:


print("RDFLIB")

for c in [NS.Person, NS.Animal]:
    for s, p, o in g.triples((None, RDF.type, c)):
        for s2, p2, o2 in g.triples((s, None, None)):
            print(s2, p2, o2)


print("SPARQL")

combined_query = prepareQuery('''
    SELECT ?Subject ?p ?o WHERE {
        {
            ?Subject rdf:type ns:Animal.
        } UNION {
            ?Subject rdf:type ns:Person.
        }
        ?Subject ?p ?o
    }
    ''',
                              initNs={"rdfs": RDFS, "ns": NS, "rdf": RDF}
                              )

# Execute the combined query
for result in g.query(combined_query):
    print(result.Subject, result.p, result.o)


# **TASK 7.4:  List the name of the persoNS who know Rocky**

# In[7]:


print("RDFLib:")
for s, p, o in g.triples((None, RDF.type, NS.Person)):
    for s2, p2, o2 in g.triples((s, FOAF.knows, NS.RockySmith)):
        print(s2)

print("SPARQL:")
q4 = prepareQuery('''
  SELECT ?Subject ?p ?o WHERE {
    ?Subject rdf:type ns:Person.
    ?Subject foaf:knows ns:RockySmith
  }
  ''',
                  initNs={"foaf": FOAF, "ns": NS, "rdf": RDF}
                  )
for ns in g.query(q4):
    print(ns.Subject)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[11]:


print("RDFLib:")

entity_counts = Counter()

for s, p, o in g.triples((None, FOAF.knows, None)):
    entity_counts[s] += 1

for entity, count in entity_counts.items():
    if count >= 2:
        print(f"{entity}: knows {count} times")

print("SPARQL:")

q5 = prepareQuery('''
    SELECT ?Subject WHERE {
        ?Subject foaf:knows ?p1, ?p2.
        FILTER (?p1 != ?p2)
    }
''',
                  initNs={"foaf": FOAF}
                  )

entities = set()

for row in g.query(q5):
    entities.add(row.Subject)

for entity in entities:
    print(f"Entity {entity} knows at least 2 other entities")
