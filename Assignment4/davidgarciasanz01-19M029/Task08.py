#!/usr/bin/env python
# coding: utf-8

# **Task 08: Completing missing data**

# In[1]:


get_ipython().system(u'pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# In[2]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")


# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# In[3]:


ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
data = Namespace('http://data.org#')

query = """
SELECT ?person
WHERE {{
   ?person rdf:type foaf:Person .
}}
"""

results = g1.query(query)
properties_to_complete = [vcard.givenName, vcard.familyName, vcard.email]

for person_uri in results:
    person = person_uri[0]

    for prop in properties_to_complete:
        if not g1.value(person, prop):
            value_from_g2 = g2.value(person, prop)
            if value_from_g2:
                g1.add((person, prop, value_from_g2))


print(g1.serialize(format="ttl"))







# In[ ]:




