#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[3]:


from rdflib.plugins.sparql import prepareQuery

for s, p, o in g:
  print(s,p,o)


# In[4]:


# TO DO
# Visualize the results
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
    SELECT ?subClass
    WHERE {
        ?subClass rdfs:subClassOf/rdfs:subClassOf* ns:LivingThing.
    }
""", initNs={"ns": Namespace("http://somewhere#"), "rdfs": RDFS})

for r in g.query(q1):
  print(r.subClass)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[5]:


# TO DO
# Visualize the results
q1 = prepareQuery("""
    SELECT ?individuals
    WHERE {
        ?individuals rdf:type/rdfs:subClassOf* ns:Person.
    }
""", initNs={"ns": Namespace("http://somewhere#"), "rdf": RDF, "rdfs": RDFS})

for r in g.query(q1):
  print(r.individuals)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[6]:


# TO DO
# Visualize the results
q1 = prepareQuery("""
    SELECT ?individual ?property
    WHERE {
        ?individual rdf:type ?class.
        FILTER (?class = ns:Person || ?class = ns:Animal)
        ?individual ?property ?value.
    }
""", initNs={"ns": Namespace("http://somewhere#"), "rdf": RDF})

# Execute the query and print the results
for r in g.query(q1):
    print("Individual:")
    print(r.individual)
    print("\tProperty")
    print("\t"+r.property)  
  


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[7]:


# Define the SPARQL query
q1 = prepareQuery("""
    SELECT ?person
    WHERE {
        ?person rdf:type/rdfs:subClassOf* ns:Person;
         foaf:knows ns:RockySmith.
    }
""", initNs={"ns": Namespace("http://somewhere#"), 
             "vcard": Namespace("http://www.w3.org/2001/vcard-rdf/3.0/"), 
             "foaf": Namespace("http://xmlns.com/foaf/0.1/"), 
             "rdf": RDF, "rdfs": RDFS})

# Execute the query and print the results
for r in g.query(q1):
    print(r.person)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[8]:


# TO DO
q2 = prepareQuery('''
    SELECT ?entities 
    WHERE {
        ?entities foaf:knows ?entity1;
         foaf:knows ?entity2.
        FILTER (?entity1 != ?entity2)
    }
    GROUP BY ?entities
    HAVING ((COUNT(DISTINCT ?entity1) + COUNT(DISTINCT ?entity)) >= 2)
    
''', initNs={"foaf": Namespace("http://xmlns.com/foaf/0.1/")})

# Visualize the results
for row in g.query(q2):
    print(row.entities)

