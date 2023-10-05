#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[2]:


get_ipython().system(u'pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[19]:


from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS,FOAF
ns=Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[5]:


from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT ?SubClass WHERE { 
    ?SubClass rdfs:subClassOf ns:Person.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": Namespace("http://somewhere#")}
)


# Visualize the results

for r in g.query(q1):
  print(r)


# In[6]:


for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(s)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[7]:


# TO DO
# Visualize the results
q2 = prepareQuery('''
  SELECT ?instance WHERE { 
    ?instance a ?type.
    ?type rdfs:subClassOf* ns:Person
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": Namespace("http://somewhere#")}
)


# Visualize the results

for r in g.query(q2):
  print(r)


# In[8]:


for s,p,o in g.triples((None, RDF.type, None)):
    for s0,p0,o0 in g.triples((o, RDFS.subClassOf, ns.Person)):
        print(s)
    for _,_,_ in g.triples((s, RDF.type, ns.Person)):
        print(s)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[14]:


# TO DO
# Visualize the results
q3 = prepareQuery('''
  SELECT ?instance ?p ?o WHERE { 
    { ?instance a ns:Person. }
    UNION
    { ?instance a ns:Animal. }
    ?instance ?p ?o
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": Namespace("http://somewhere#")}
)


# Visualize the results

for r in g.query(q3):
  print(r)


# In[15]:


for clase in [ ns.Person, ns.Animal ]:
    for s, _, _ in g.triples((None, RDF.type, clase)):
        for _, p, v in g.triples((s, None, None)):
            print(s, clase, p, v)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[22]:


# TO DO
# Visualize the results
q = prepareQuery('''
  SELECT ?person WHERE { 
    ?person foaf:knows [ vcard:Given "Rocky"^^xsd:string ].
  }
  ''',
  initNs = { "foaf": FOAF, "vcard": vcard, "xsd": XSD}
)

for r in g.query(q):
  print(r)


# In[20]:



for rocky, _, _ in g.triples((None, vcard.Given, Literal('Rocky', datatype = XSD.string))):
    for person, _, _ in g.triples((None, FOAF.knows, rocky)):
        print(person)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[29]:


# TO DO
# Visualize the results
q5= prepareQuery('''
  SELECT DISTINCT ?entities  WHERE 
  {
    ?entities foaf:knows ?otherEntities.
    FILTER(?entities != ?otherEntities).
  } GROUP BY ?entities
    HAVING (COUNT(?otherEntities) >1)
  ''',
  initNs = {"foaf":FOAF}
)
for r in g.query(q5):
  print(r)


# In[ ]:





# In[ ]:




