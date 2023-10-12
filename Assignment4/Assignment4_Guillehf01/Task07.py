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

ns = Namespace("http://somewhere#")
contRDFLib = 0
contSPARQL = 0

#RDFLib
print("RDFLib Query:")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    contRDFLib+=1
    print(f'Subclass {contRDFLib}: {s}')

print("\n")
print("SPARQL Query:")
#SPARQL
q1 = prepareQuery('''
  SELECT ?Subclass WHERE { 
    ?Subclass rdfs:subClassOf ns:LivingThing.
  }
  ''',
  initNs = {"ns":ns, "rdfs":RDFS}
)

for r in g.query(q1):
    contSPARQL+=1
    print(f'Subclass {contSPARQL}: {r.Subclass}')


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[4]:


contRDFLib1 = 0
contRDFLib2 = 0
contSPARQL = 0

#RDFLib
print("RDFLib Query for the class Person:")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    contRDFLib1+=1
    print(f'Individual {contRDFLib1}: {s}')

print("\n")    
print("RDFLib Query for the subclass Person:")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for ss, ps, os in g.triples((None, RDF.type, s)):
        contRDFLib2+=1
        print(f'Individual {contRDFLib2}: {ss}')

print("\n")
print("SPARQL Query:")
#SPARQL
q2 = prepareQuery('''
  SELECT ?Individuals WHERE { 
    ?sub rdfs:subClassOf* ns:Person.
    ?Individuals rdf:type ?sub.
  }
  ''',
  initNs = {"ns":ns, "rdfs":RDFS, "rdf":RDF}
)

for r in g.query(q2):
    contSPARQL+=1
    print(f'Sub/class {contSPARQL}: {r.Individuals}')


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[44]:


from collections import defaultdict

contRDFLibInst = 0
contSPARQL = 0

#RDFLib
print("RDFLib Query:")
individuals = set()

for s, p, o in g.triples((None, RDF.type, None)):
    if o == ns.Person or o == ns.Animal:
        individuals.add(s)

for individual in individuals:
    contRDFLibInst+=1
    print(f'Instance {contRDFLibInst}: {individual}')
    for s, p, o in g.triples((individual, None, None)):
        print(f'  Property: {p}, Value: {o}')
        
print("\n")
print("SPARQL Query:")
#SPARQL
q4 = prepareQuery('''
  SELECT ?individual ?property ?value WHERE {
    ?individual rdf:type ?class .
    ?individual ?property ?value .
    FILTER (?class = ns:Person || ?class = ns:Animal)
  }
  ''', initNs={"rdf": RDF, "ns": ns})

result_dict = defaultdict(lambda: defaultdict(list))

for row in g.query(q4):
    result_dict[row.individual][row.property].append(row.value)

for individual, properties in result_dict.items():
    contSPARQL+=1
    print(f'Instance {contSPARQL}: {individual}')
    for property, values in properties.items():
        print(f'  Property: {property}', end=' ')
        print(', '.join(f'Value: {value}' for value in values))


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[45]:


from rdflib import XSD

contRDFLib = 0
contSPARQL = 0
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

#RDFLib
print("RDFLib Query:")
for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
    for ss, ps, os in g.triples((s, VCARD.Given, None)):
        contRDFLib+=1
        print(f'Person {contRDFLib}: {os}')
    
print("\n")
print("SPARQL Query:")
#SPARQL
q4 = prepareQuery('''
  SELECT ?Given  WHERE {
    ?Subject foaf:knows ?RockySmith.
    ?RockySmith vcard:FN ?RockySmithFullName.
    ?Subject vcard:Given ?Given.
  }  
  ''',
  initNs = { "foaf": FOAF, "vcard": VCARD}
)

for r in g.query(q4, initBindings = {'?RockySmithFullName' : Literal('Rocky Smith', datatype=XSD.string)}):
    contSPARQL+=1
    print(f'Person {contSPARQL}: {r.Given}')


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[56]:


contRDFLib = 0
contSPARQL = 0

#RDFLib
print("RDFLib Query:")
entity_count = {}

for s, p, o in g.triples((None, FOAF.knows, None)):
    if s in entity_count:
        entity_count[s] += 1
    else:
        entity_count[s] = 1

for entity, count in entity_count.items():
    if count >= 2:
        contRDFLib+=1
        print(f'Entity {contRDFLib}: {entity}')

print("\n")
print("SPARQL Query:")
#SPARQL
q5 = prepareQuery('''
  SELECT ?entity WHERE {
    ?entity foaf:knows ?entity1 .
    ?entity foaf:knows ?entity2 .
    FILTER (?entity1 != ?entity2)
  }
  GROUP BY ?entity
  HAVING (COUNT(?entity1) >= 2)
  ''',
  initNs = {"foaf":FOAF}
)

for r in g.query(q5):
    contSPARQL+=1
    print(f'Entity {contSPARQL}: {r.entity}')


# In[ ]:




