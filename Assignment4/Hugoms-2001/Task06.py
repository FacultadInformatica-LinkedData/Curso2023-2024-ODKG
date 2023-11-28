#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Task 06: Modifying RDF(s)


# In[1]:


get_ipython().system('pip install rdflib')


# In[2]:


github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# In[3]:


# Read the RDF file as shown in class
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# In[4]:


# Create a new class named Researcher
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# In[5]:


# TASK 6.1: Create a new class named "University"
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[6]:


# TASK 6.2: Add "Researcher" as a subclass of "Person"
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[7]:


#TASK 6.3: Create a new individual of Researcher named "Jane Smith"
g.add((ns.JaneSmith, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[11]:


#TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g.add((ns.JaneSmith, VCARD.Email, Literal("jsmith@example.org")))
g.add((ns.JaneSmith, VCARD.FN, Literal("Jane Smith")))
g.add((ns.JaneSmith, VCARD.Given, Literal("Jane")))
g.add((ns.JaneSmith, VCARD.Family, Literal("Smith")))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[12]:


#TASK 6.5: Add UPM as the university where John Smith works
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, ns.work, ns.UPM))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[13]:


#Task 6.6: Add that Jown knows Jane using the FOAF vocabulary
from rdflib import FOAF
g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

