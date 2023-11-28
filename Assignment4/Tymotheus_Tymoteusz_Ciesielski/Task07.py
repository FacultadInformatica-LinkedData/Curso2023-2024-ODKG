#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[3]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[4]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[5]:


from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
query_text = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://somewhere#>
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
"""
q1 = prepareQuery(query_text)

for r in g.query(q1):
    print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[6]:


query_text = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://somewhere#>
    SELECT ?individual
    WHERE {
        ?individual rdf:type ?type .
        ?type rdfs:subClassOf* ns:Person .
    }
"""
q2 = prepareQuery(query_text)
for r in g.query(q2):
    print(r)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[7]:


query_text = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://somewhere#>
    SELECT distinct ?individual ?property ?value
    WHERE {
        ?individual rdf:type ?class .
        ?individual ?property ?value .
        FILTER (?class = ns:Person || ?class = ns:Animal) .
    }
"""
q3 = prepareQuery(query_text)
for r in g.query(q3):
    print(r)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[17]:


ns = Namespace("http://somewhere#")
query_text = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>
    PREFIX ns: <http://somewhere#>
    SELECT  ?Subject ?Given  WHERE {
    ?Subject foaf:knows ?RockySmith.
	?RockySmith vcard:Given ?Rocky.
	?Subject vcard:Given ?Given.
  }
"""
q4 = prepareQuery(query_text)
for r in g.query(q4):
    print(r)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[19]:


ns = Namespace("http://somewhere#")
query_text = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>
    SELECT ?Given  WHERE {
    ?Subject foaf:knows ?RockySmith.
    ?RockySmith vcard:FN ?RockySmithFullName.
    ?Subject vcard:Given ?Given.
  }
"""
q5 = prepareQuery(query_text)

for r in g.query(q5):
    print(r)


# In[ ]:




