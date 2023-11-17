# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
from rdflib.plugins.sparql import prepareQuery


VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
NS = Namespace("http://somewhere#")

q1 = prepareQuery('''
  SELECT ?subClass WHERE { 
    ?subClass rdfs:subClassOf* ns:LivingThing. 
  }
  ''',
  initNs = { "vcard": VCARD, "rdfs":RDFS, "ns":NS}
)

# Visualize the results
for r in g.query(q1):
  print(r.subClass)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
q2 = prepareQuery('''
  SELECT ?individual WHERE { 
    {
      ?individual rdf:type ?subClass. 
      ?subClass rdfs:subClassOf* ns:Person.
    }
    UNION
    {
      ?individual rdf:type ns:Person.
    } 
  }
  ''',
  initNs = { "vcard": VCARD, "rdfs":RDFS, "ns":NS}
)


# Visualize the results
for r in g.query(q2):
  print(r.individual)


# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %%
q3 = prepareQuery('''
  SELECT ?personOrAnimal ?properties ?value
    WHERE {
        ?personOrAnimal rdf:type ?class.
        ?personOrAnimal ?properties ?value. #Properties for the individual
        
        { ?personOrAnimal rdf:type ns:Person. } #Persons
        UNION
        { ?personOrAnimal rdf:type ns:Animal .} #Animals
    }
  ''',
  initNs = { "vcard": VCARD, "rdfs":RDFS, "ns":NS}
)


# Visualize the results
for r in g.query(q3):
  print(r.personOrAnimal, r.properties, r.value)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %%
from rdflib.namespace import FOAF
q4= prepareQuery('''
  SELECT ?personsWhoKnowRocky WHERE { 
  {
    ?personsWhoKnowRocky foaf:knows ?rockyURI.
    ?rockyURI vcard:FN ?rockyFN.
    FILTER(?rockyFN = "Rocky Smith")
    {
      ?personsWhoKnowRocky rdf:type ?subClass. 
      ?subClass rdfs:subClassOf ns:Person.
    }
    UNION
    {
      ?personsWhoKnowRocky rdf:type ns:Person.
    } 
  }
}
  ''',
  initNs = { "vcard": VCARD.replace("#","/"), "rdfs":RDFS, "ns":NS, "foaf":FOAF}
)


# Visualize the results
for r in g.query(q4):
  print(r.personsWhoKnowRocky)

# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %%
entities_dictionary = {} #dictionary to store the known entities
for s, p, o in g.triples((None, FOAF.knows, None)):
  if s != o: #knows other individual, not itself
    if s in entities_dictionary:
      entities_dictionary[s] += 1 #increment the number of known entities for this entity
    else:
      entities_dictionary[s] = 1 #add the entity to the dictionary

# Visualize the results
for key, value in entities_dictionary.items():
  if key >= 2:
    print('Entity:', key, 'knows', value, 'other entities')
    