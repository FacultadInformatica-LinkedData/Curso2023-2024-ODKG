#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[54]:


get_ipython().system(u'pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[55]:


from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS,FOAF
ns=Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[56]:


from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT ?SubClass WHERE { 
    ?SubClass rdfs:subClassOf+ ns:LivingThing.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": Namespace("http://somewhere#")}
)


# Visualize the results
print("SPARQL results:")
for r in g.query(q1):
  print(r)


# In[57]:


def get_subclases_anidadas(clase_padre, grafo):
    subclases = set()
    for subclase, _, _ in grafo.triples((None, RDFS.subClassOf, clase_padre)):
        subclases.add(subclase)
        subclases.update(get_subclases_anidadas(subclase, grafo))
    return subclases

# Visualizar los resultados
print("RDFLIB results:")
living_thing_subclases = get_subclases_anidadas(ns.LivingThing, g)
for subclase in living_thing_subclases:
    print(subclase)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[58]:


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
print("SPARQL results:")
for r in g.query(q2):
  print(r)


# In[59]:


def get_instances(class_, grafo):
    instances = set()
    for s, p, o in grafo.triples((None, RDF.type, class_)):
        instances.add(s)
        sub_classes = get_subclases_anidadas(class_, grafo)
        for sub_class in sub_classes:
            for s, p, o in grafo.triples((None, RDF.type, sub_class)):
                instances.add(s)
    return instances

# Llamar a la función para obtener instancias de ns:Person sin tipos de subclase
people_without_types = get_instances(ns.Person, g)

# Visualizar los resultados
print("RDFLIB results:")
for person in people_without_types:
    print(person)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[60]:


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
print("SPARQL results:")
for r in g.query(q3):
  print(r)


# In[61]:


print("RDFLIB results:")
for clase in [ ns.Person, ns.Animal ]:
    for s, _, _ in g.triples((None, RDF.type, clase)):
        for _, p, v in g.triples((s, None, None)):
            print(s, clase, p, v)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[62]:


q = prepareQuery('''
  SELECT ?full_name
  WHERE { 
    ?individual RDF:type/rdfs:subClassOf* ns:Person.
  ?individual FOAF:knows ns:RockySmith.
  ?individual vcard:FN ?full_name
  }
''', initNs={"FOAF": FOAF, "RDFS": RDFS, "RDF": RDF, "ns": ns, "vcard": vcard}
)

# Visualize the results
print("SPARQL results:")
for r in g.query(q):
    print(r[0])


# In[63]:


print("RDFLIB results:")
for rocky, _, _ in g.triples((None, vcard.Given, Literal('Rocky', datatype = XSD.string))):
    for person, _, _ in g.triples((None, FOAF.knows, rocky)):
        print(person)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[64]:


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
print("SPARQL results:")
for r in g.query(q5):
  print(r)


# In[65]:


from collections import defaultdict


entidades_conocidas = defaultdict(set)

for s, p, o in g.triples((None, FOAF.knows, None)):
    entidades_conocidas[s].add(o)

entidades_conocen_almenos_dos = [entidad for entidad, conocidos in entidades_conocidas.items() if len(conocidos) >= 2]

print("RDFLIB results:")
for entidad in entidades_conocen_almenos_dos:
    print(entidad)


# In[ ]:




