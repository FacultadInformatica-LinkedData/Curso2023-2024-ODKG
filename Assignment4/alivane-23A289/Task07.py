#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[75]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[78]:


from rdflib import Graph, Namespace, Literal, FOAF
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[128]:


# DONE
ns = Namespace("http://somewhere#")

LivingThing = ns.LivingThing

print("QUERY RDFLib")
subclasses_of_lt = set()
def find_subclasses(subclass, graph, subclasses):
    for s, _, _ in graph.triples((None, RDFS.subClassOf, subclass)):
        if s not in subclasses:
            subclasses.add(s)
            find_subclasses(s, graph, subclasses)


find_subclasses(LivingThing, g, subclasses_of_lt)

# Print the subclasses results
for subclass in subclasses_of_lt:
    print(subclass)


print("QUERY SPARQL")
# Visualize the results
q1 = prepareQuery('''
    SELECT ?s
    WHERE {
        ?s RDFS:subClassOf+ ns:LivingThing .
    }
    ''',
    initNs = {
        'RDFS': RDFS,
        'ns': ns
    }
)
for r in g.query(q1):
  print(r.s)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[127]:


# DONE
print("QUERY RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s)

for subclasses, sP, sO in g.triples((None, RDFS.subClassOf, ns.Person)):
    for person, pP, pO in g.triples((None, RDF.type, subclasses)):
        print(person)


print("QUERY SPARQL")
q2 = prepareQuery('''
    SELECT DISTINCT ?individual
    WHERE {
        {
            ?individual RDF:type ns:Person .
        }
        UNION {
            ?s RDFS:subClassOf* ns:Person .
            ?individual RDF:type ?s .
        }         
    }
    ''',
    initNs={
        'ns': ns,
        'RDF': RDF,
        'RDFS': RDFS
    }
)
# Visualize the results
for r in g.query(q2):
    print(r.individual)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[191]:


#DONE
print("QUERY RDFLib")
# Person
for s1, _, _ in g.triples((None, RDF.type, ns.Person)):
    for _, p2, _ in g.triples((s1, None, None)):
        print(s1, p2)

for s1, _, _ in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s2, _, _ in g.triples((None, RDF.type, s1)):
        for s3, p3, _ in g.triples((s2, None, None)):
            print(s3, p3)

# Animals
for s1, _, _ in g.triples((None, RDF.type, ns.Animal)):
    for _, p2, _ in g.triples((s1, None, None)):
        print(s1, p2)

for s1, _, _ in g.triples((None, RDFS.subClassOf, ns.Animal)):
    for s2, _, _ in g.triples((None, RDF.type, s1)):
        for s3, p3, _ in g.triples((s2, None, None)):
            print(s3, p3)


# In[194]:


# Visualize the results
print("QUERY SPARQL")
q3 = prepareQuery('''
    SELECT DISTINCT ?s ?p
    WHERE {
        {
            ?s RDF:type ns:Person .
        }
        UNION
        {
            ?su RDFS:subClassOf* ns:Person .
            ?s RDF:type ?su .
        }
        UNION
        {
            ?s RDF:type ns:Animal .
        }
        UNION
        {
            ?su RDFS:subClassOf* ns:Animal .
            ?s RDF:type ?su .
        }
        ?s ?p ?o
    }
    ''',
    initNs={
        'ns': ns,
        'RDF': RDF,
        'RDFS': RDFS
    }
)

for r in g.query(q3):
    print(r.s, r.p)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[222]:


# DONE
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

print("QUERY RDFLib")

def is_subcperson(class_uri):
  for s, p, o in g.triples((class_uri, RDFS.subClassOf, None)):
    if o == ns.Person or is_subcperson(o):
      return True
  return False

rockyUri = None
for s, _, _ in g.triples((None, VCARD.Given, Literal("Rocky"))):
  rockyUri = s

names_knows_rocky = set()
for s, _, _ in g.triples((None, FOAF.knows, rockyUri)):
  for _, _, t in g.triples((s, RDF.type, None)):
    if t == ns.Person or is_subcperson(t):
      for _, _, name in g.triples((s, VCARD.Given, None)):
        names_knows_rocky.add(name)

# Visualize the results
for name in names_knows_rocky:
  print(name)


print("QUERY SPARQL")

q4 = prepareQuery('''
  SELECT DISTINCT ?nameKnowsRocky 
   WHERE {
      ?s vcard:Given ?o.
      ?knowsSubject FOAF:knows ?s.
      ?knowsSubject vcard:Given ?nameKnowsRocky.
      { 
        ?knowsSubject rdf:type ns:Person .
      }
      UNION
      { 
        ?knowsSubject rdf:type ?type .
        ?type rdfs:subClassOf* ns:Person . 
      }
   }
  ''',
  initNs={
      "rdfs":RDFS, 
      "ns":ns, 
      "FOAF":FOAF, 
      "rdf":RDF,
      "vcard": VCARD, 
  }
)

for r in g.query(q4):
  print(r.nameKnowsRocky)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[246]:


# DONE
print("QUERY RDFLib")
entities = {}
# Visualize the results
for s, p, o in g.triples((None, FOAF.knows, None)):
    if s in entities:
        entities[s] = entities[s] + 1
    else:
        entities[s] = 1
for entity in entities:
    if entities[entity] > 1:
        print(f"Entity: {entity}, Total knows: {entities[entity]}")

print("QUERY SPARQL")
q5 = prepareQuery('''
    SELECT DISTINCT ?s (COUNT(?o) as ?total_knows) 
    WHERE 
    {
        ?s FOAF:knows ?o.
        FILTER(?s != ?o).
    } 
    GROUP BY ?s
    HAVING (COUNT(?o) >= 2)
    ''',
    initNs={
        'FOAF': FOAF
    }
)

for r in g.query(q5):
    print(f"Entity: {r.s}, Total knows: {r.total_knows}")


