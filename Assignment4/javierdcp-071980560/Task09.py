#!/usr/bin/env python
# coding: utf-8

# **Task 09: Data linking**

# In[17]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"


# In[18]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")


# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# In[19]:


get_ipython().system('pip install ontospy')


# In[20]:


for s, p, o in g1.triples((None, VCARD.FN, None)):
  print(s,p,o)


# In[21]:


for s, p, o in g2.triples((None, VCARD.FN, None)):
  print(s,p,o)


# In[22]:


from ontospy import Ontospy

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

for s1, p1, o1 in g1.triples((None, VCARD.FN, None)):
    print(s1,p1,o1,"1")
    for s2, p2, o2 in g2.triples((None, VCARD.FN, None)):
        
        if o1==o2:
            g3.add((s1, OWL.sameAs, s2))
            print(s2,p2,o2,"2")
            print(s1,s2)
            


# In[ ]:




