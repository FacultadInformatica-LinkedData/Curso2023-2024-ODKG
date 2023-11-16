# %% [markdown]
# **Task 08: Completing missing data**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF,FOAF
from rdflib.plugins.sparql import prepareQuery
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

# %% [markdown]
# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# %% [markdown]
# #### Task 1: List all the Persons of the first graph and  look for their properties

# %%
dt = Namespace("http://data.org#")
persons = []

#List all the persons of the first graph
for s,p,o in g1.triples((None,RDF.type,dt.Person)):

    print(f'Subject {s}, Predicate {p} , Object {o}')
    persons.append(s)
    
#Dictionary of properties
dic = {}
#Find the properties of the persons in the first graph and their values
#Save the properties and values on a dictionary
for person in persons:

    dic[person] = {}
    for s,p,o in g1.triples((person,None,None)):

        print(f"Property: {p} Value {o}")
        
        dic[person][p] = o



# %% [markdown]
# #### Task 2. Check missing properties and mismatches between the first graph and the second

# %%
#Dictionary for missing properties
dic_missing = {}

#List all the persons of the second graph
for s,p,o in g2.triples((None,RDF.type,dt.Person)):
    print(f'Subject {s}, Predicate {p} , Object {o}')
    #If the person of the second graph is also in the first then check its properties
    if s in persons:
        dic_missing[s] = {}
        for s2,p2,o2 in g2.triples((s,None,None)):
        
            print(f"Property: {p2}, value: {o2}")
            #Check if the person has also that property on the first graph
            if p2 not in dic[s2].keys():

                #Add the property and value to the missing property dictionary
                print(f"Missing property: {p2}, value: {o2}")
                dic_missing[s2][p2] = o2

            #Just tell if the person's property has a different value on both graphs
            elif dic[s2][p2] != o2:
                print(f"Different value for property {p2}")
    


# %% [markdown]
# #### Task 3. Add the missing properties on the first graph

# %%
#Iterate over the persons that have missing properties
for person in dic_missing.keys():
    #Iterate over the missing properties of that person
    for missing in dic_missing[person].keys():
        #Add the property to the first graph
        value = dic_missing[person][missing]
        g1.add((person, missing, value))
        print(f"Added property {missing} with value {value} for: {person}.")


# %% [markdown]
# #### Task 4: Print again the properties of all persons in graph 1
# This time using `SPARQL` on `RDFLib`
# 

# %%
# Define query
g1.bind('dt',dt)
g1.bind('rdf',RDF)

query_text = """
    SELECT ?individual ?property ?value
    WHERE {
        ?individual rdf:type dt:Person .
        ?individual ?property ?value .
    }
"""
# prepare query
query = prepareQuery(query_text, initNs={'dt':dt,'rdf':RDF})

# Execute the query
# Visualize the results
for row in g1.query(query):
    print(f'Person: {row[0]}, Property: {row[1]}, Value: {row[2]}')




