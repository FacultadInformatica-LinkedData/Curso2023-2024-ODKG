#!/usr/bin/env python
# coding: utf-8

# **Task 09: Data linking**

# In[1]:


get_ipython().system(u'pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"


# In[2]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")


# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# In[6]:


from rdflib.namespace import OWL, RDF

ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
three = Namespace("http://data.three.org#")
owl = Namespace("http://www.w3.org/2002/07/owl#")


# In[18]:




apodos_g1 = set(g1.objects(None, vcard.given))
apodos_g2 = set(g2.objects(None, vcard.given))
nombres_familia_g1 = set(g1.objects(None, vcard.family))
nombres_familia_g2 = set(g2.objects(None, vcard.family))

for apodo in apodos_g1.intersection(apodos_g2):
    for nombre_familia in nombres_familia_g1.intersection(nombres_familia_g2):
        individuo_g1 = list(g1.subjects(ns.vcard.nickname, apodo))[0]
        individuo_g2 = list(g2.subjects(ns.vcard.nickname, apodo))[0]

        g3.add((individuo_g1, OWL.sameAs, individuo_g2))
print(g3.serialize(format="ttl"))


# In[12]:





# In[17]:





# In[ ]:





# In[ ]:




