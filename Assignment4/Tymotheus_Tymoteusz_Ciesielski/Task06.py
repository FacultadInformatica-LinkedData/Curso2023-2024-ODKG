#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[10]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# Create a new class named Researcher

# In[11]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.1: Create a new class named "University"**
# 

# In[12]:


g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[13]:


g.add((ns.Person, RDF.type, RDFS.Class))
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**

# In[14]:


janeURI = ns.JaneSmith

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")


g.add((janeURI, RDFS.Class, ns.Researcher))

for s, p, o in g:
  print(s,p,o)


# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**

# In[16]:


fullName = Literal("Jane Smith")
g.add((ns.JaneSmith, VCARD.EMAIL, Literal("janey@example.org")))
g.add((ns.JaneSmith, VCARD.FN, fullName))
g.add((ns.JaneSmith, VCARD.FAMILY, Literal("Smith") ))
g.add((ns.JaneSmith, VCARD.GIVEN, Literal("Jane") ))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.5: Add UPM as the university where John Smith works**

# In[17]:


john_smith = ns.JohnSmith
upm = ns.UPM
g.add((upm, RDF.type, ns.University))
g.add((john_smith, VCARD.ORG, upm))
g.add((upm, RDFS.label, Literal("Universidad Politécnica de Madrid")))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**

# In[9]:


from rdflib import FOAF
g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

