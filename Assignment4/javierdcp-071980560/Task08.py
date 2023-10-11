#!/usr/bin/env python
# coding: utf-8

# **Task 08: Completing missing data**

# In[32]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# In[33]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")


# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# In[34]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
vcard= Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns = Namespace("http://data.org#")

#Ver g1
for s, p, o in g1.triples((None, RDF.type, ns.Person)):
  for s0, p0, o0 in g1.triples((s, None, None)):
    print(s0, p0, o0)


# In[35]:


#Ver g2
for s, p, o in g2.triples((None, RDF.type, ns.Person)):
    for s0, p0, o0 in g2.triples((s, None, None)):   
        print(s0,p0, o0)


# In[37]:


#Añadir a g1 los datos de g2
for s, p, o in g1.triples((None, RDF.type, ns.Person)):
    for s0, p0, o0 in g2.triples((s, vcard.Given, None)):
        g1.add((s0, vcard.Given, o0))
    for s1, p1, o1 in g2.triples((s, vcard.Family, None)):
        g1.add((s1, vcard.Family, o1))
    for s2, p2, o2 in g2.triples((s, vcard.FN, None)):
        g1.add((s2, vcard.FN, o2))
    for s3, p3, o3 in g2.triples((s, vcard.EMAIL, None)):
        g1.add((s3, vcard.EMAIL, o3))


# In[38]:


#Ver g1 completo
for s, p, o in g1.triples((None, RDF.type, ns.Person)):
    for ss, pp, oo in g1.triples((s, None, None)):
        print(ss, pp, oo)

