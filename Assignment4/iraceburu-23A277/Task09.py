#!/usr/bin/env python
# coding: utf-8

# **Task 09: Data linking**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"


# In[2]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")


# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# In[3]:


def SPARQLqueries():
    q1 = prepareQuery("""
            SELECT ?valueName ?valueFamily
            WHERE {
                ?individual vcard:Given ?valueName;
                 vcard:Family ?valueFamily.
            }
            """, initNs={"vcard":"http://www.w3.org/2001/vcard-rdf/3.0#"})
    q2 = prepareQuery("""
            SELECT ?individual 
            WHERE {
                ?individual vcard:Given ?valueName;
                 vcard:Family ?valueFamily.
            }
            """, initNs={"vcard":"http://www.w3.org/2001/vcard-rdf/3.0#"})

   
    return q1,q2


# In[4]:


for s,p,o in g1:
    print(s, p, o)


# In[5]:



for s,p,o in g2:
    print(s, p, o)


# In[6]:


for s,p,o in g3:
    print(s, p, o)


# In[7]:


from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import OWL

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")


g1Individuals = []
g2Individuals = []

q = SPARQLqueries()
print("Values in graph1: ")
for r1 in g1.query(q[0]):
    print("\t\t- "+r1.valueName+ " "+ r1.valueFamily)
    g1Individuals.append([r1.valueName, r1.valueFamily])

print("Values in graph2: ")
for r2 in g2.query(q[0]):
    print("\t\t- "+r2.valueName+" " +r2.valueFamily)
    g2Individuals.append([r2.valueName, r2.valueFamily])


comun_element = [element for element in g1Individuals if element in g2Individuals]
for element in comun_element:
    print("\nSame in both graphs: ")
    print(element[0]+" "+ element[1])
    
    for r3 in g1.query(q[1], initBindings={ "valueName":element[0], "valueFamily": element[1]}):
        print("\tGraph1 URI:")
        print(r3.individual)
    for r4 in g2.query(q[1], initBindings={ "valueName":element[0], "valueFamily": element[1]}):
        print("\tGraph2 URI:")
        print(r4.individual)
        
    g3.add((r3.individual,OWL.sameAs,r4.individual))
    

print("\n\tThe new graph3")
for s,p,o in g3:
    print(s, p, o)

