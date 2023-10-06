#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[2]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[3]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[8]:


# RDFLib
ns = Namespace("http://somewhere#")    

# Visualize the results
for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    print(s)


# In[9]:


# SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?s WHERE { 
    ?s RDFS:subClassOf ns:LivingThing . 
  }
  ''',
  initNs = {"RDFS":RDFS, "ns": ns}
)

# Visualize the results
for r in g.query(q1):
 print(r.s)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[14]:


# RDFLib
ns = Namespace("http://somewhere#")    

# Individuals of "Person"
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)

# Individuals of the subclases of "Person"
for subclass,_,_ in g.triples((None, RDFS.subClassOf, ns.Person)):
    for ind,_,_ in g.triples((None, RDF.type, subclass)):
        print(ind)


# In[17]:


# SPARQL
q2 = prepareQuery('''
  SELECT DISTINCT ?ind WHERE { 
    {
    ?ind RDF:type ns:Person . 
    } UNION {
    ?s RDFS:subClassOf* ns:Person .
    ?ind RDF:type ?s .
    }
  }
  ''',
  initNs = {"RDF":RDF, "RDFS":RDFS, "ns": ns}
)

# Visualize the results
for r in g.query(q2):
 print(r.ind)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[35]:


# RDFLib
# Individuals of "Person"
for s1,p1,o1 in g.triples((None, RDF.type, ns.Person)):
    for s2,p2,o2 in g.triples((s1, None, None)):
        print(s2, p2)

# Individuals of the subclases of "Person"
for s1,p1,o1 in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s2,p2,o2 in g.triples((None, RDF.type, s1)):
        for s3,p3,o3 in g.triples((s2, None, None)):
            print(s3,p3)

# ---------------------------------
# Individuals of "Animal"
for s1,p1,o1 in g.triples((None, RDF.type, ns.Animal)):
    for s2,p2,o2 in g.triples((s1, None, None)):
        print(s2, p2)
        
# Individuals of the subclases of "Animal"
for s1,p1,o1 in g.triples((None, RDFS.subClassOf, ns.Animal)):
    for s2,p2,o2 in g.triples((None, RDF.type, s1)):
        for s3,p3,o3 in g.triples((s2, None, None)):
            print(s3,p3)


# In[37]:


# SPARQL
q3 = prepareQuery('''
  SELECT DISTINCT ?ind ?prop WHERE { 
    {
    ?ind RDF:type ns:Person . 
    } UNION {
    ?s RDFS:subClassOf* ns:Person .
    ?ind RDF:type ?s .
    } UNION  {
    ?ind RDF:type ns:Animal . 
    } UNION {
    ?s RDFS:subClassOf* ns:Animal .
    ?ind RDF:type ?s .
    }
    ?ind ?prop ?obj
  }
  ''',
  initNs = {"RDF":RDF, "RDFS":RDFS, "ns": ns}
)


# Visualize the results
for r in g.query(q3):
 print(r.ind, r.prop)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[43]:


# RDFLib
# FOAF = Namespace("http://xmlns.com/foaf/0.1/")
from rdflib.namespace import FOAF
for s,p,o in g.triples((None, FOAF.knows, ns.RockySmith)):
    print(s)


# In[44]:


# SPARQL
q4 = prepareQuery('''
  SELECT ?s WHERE { 
    ?s FOAF:knows ns:RockySmith . 
  }
  ''',
  initNs = {"FOAF":FOAF, "ns": ns}
)


# Visualize the results
for r in g.query(q4):
 print(r.s)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[48]:


# RDFLib
known_counts = {}

# Iterate through the triples
for s, p, o in g.triples((None, FOAF.knows, None)):
    # If the subject is already in the dictionary, increment its count
    if s in known_counts:
        known_counts[s] += 1
    # Otherwise, initialize its count to 1
    else:
        known_counts[s] = 1

# Iterate through the dictionary and print entities that know at least two others
for entity, count in known_counts.items():
    if count >= 2:
        print(entity)


# In[46]:


# SPARQL
q5 = prepareQuery(
    """
    SELECT ?person
    WHERE {
        ?person foaf:knows ?friend1 .
        ?person foaf:knows ?friend2 .
        FILTER (?friend1 != ?friend2)
    }
    GROUP BY ?person
    HAVING (COUNT(?friend1) >= 2)
    """,
    initNs={"foaf": FOAF}
)

# Visualize the results
for r in g.query(q5):
 print(r.person)

