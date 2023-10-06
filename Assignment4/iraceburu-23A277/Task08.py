#!/usr/bin/env python
# coding: utf-8

# **Task 08: Completing missing data**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# In[2]:


from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")


# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# In[3]:


def listarElementosPersona():
    q1 = prepareQuery("""
    SELECT ?individuals
    WHERE {
        ?individuals rdf:type ns:Person.
        }
    """, initNs={"ns": Namespace("http://data.org#"), "rdf": RDF, "rdfs": RDFS})
    individuals = []
    for r in g1.query(q1):
        individuals.append(r.individuals)
        print(r.individuals)
    
    return individuals


# In[4]:


#I tried to do it in a loop but i couldn't pass the field correctly
def SPARQLqueries():
    q1 = prepareQuery("""
            SELECT ?value
            WHERE {
                ?individual vcard:Given ?value.
            }
            """, initNs={"ns": Namespace("http://data.org#"), "rdf": RDF, "rdfs": RDFS,  "vcard":"http://www.w3.org/2001/vcard-rdf/3.0#"})

    q2 = prepareQuery("""
                SELECT ?value
                WHERE {
                    ?individual vcard:Family ?value.
                }
                """, initNs={"ns": Namespace("http://data.org#"), "rdf": RDF, "rdfs": RDFS,  "vcard":"http://www.w3.org/2001/vcard-rdf/3.0#"})

    q3 = prepareQuery("""
                SELECT ?value
                WHERE {
                    ?individual vcard:EMAIL ?value.
                }
                """, initNs={"ns": Namespace("http://data.org#"), "rdf": RDF, "rdfs": RDFS,  "vcard":"http://www.w3.org/2001/vcard-rdf/3.0#"})

    return q1, q2, q3


# In[5]:


def addInGraph(individual, fieldN, value2):
    if(fieldN == 0):
        g1.add((individual, vcard.Given, value2))
    elif(fieldN == 1):
        g1.add((individual, vcard.Family, value2))
    else:
        g1.add((individual, vcard.EMAIL, value2))
    return g1


# In[6]:


from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS
from rdflib import XSD
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
individuals = listarElementosPersona()

#lista todos los elementos de la clase Person en el primer grafo (data01.rdf)


queries = SPARQLqueries()


for individual in individuals:
    print("Observing the individual")
    print( individual)
    value1 = value2= None
    
    for i, q in enumerate(queries):
        for r1 in g1.query(q, initBindings={ "individual":individual}):
            print("Valor1:")
            print("\t\t"+r1.value)
            value1 = r1.value
        for r2 in g2.query(q, initBindings={ "individual":individual}):
            print("Valor2:")
            print("\t\t"+r2.value)
            value2 = r2.value
        if value1 != value2:
            print("DIFFERENT")
            addInGraph(individual, i, value2)

        else:
            print("EQUAL->we don't do anything")

