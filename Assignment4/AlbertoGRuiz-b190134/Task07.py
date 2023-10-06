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
    ?subClass rdfs:subClassOf ns:LivingThing. 
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
      ?subClass rdfs:subClassOf ns:Person.
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
  SELECT DISTINCT ?personOrAnimal ?properties ?value WHERE { 
    { #Persons
        {
            ?personOrAnimal rdf:type ?subClass. 
            ?subClass rdfs:subClassOf ns:Person.
            ?personOrAnimal ?properties ?value
        }
        UNION
        {
            ?personOrAnimal rdf:type ns:Person.
            ?personOrAnimal ?properties ?value
        } 
    } #Persons
    UNION
    { #ANIMALS
        {
            ?personOrAnimal rdf:type ?subClass. 
            ?subClass rdfs:subClassOf ns:Animal.
            ?personOrAnimal ?properties ?value
        }
        UNION
        {
            ?personOrAnimal rdf:type ns:Animal.
            ?personOrAnimal ?properties ?value
        }
    } #ANIMALS
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
    FILTER(CONTAINS(str(?rockyFN), "Rocky"))
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
q5= prepareQuery('''
  SELECT DISTINCT ?entities (COUNT(?otherEntities) as ?numberOfKnownEntities) WHERE 
  {
    ?entities foaf:knows ?otherEntities.
    FILTER(?entities != ?otherEntities).
  } GROUP BY ?entities
    HAVING (COUNT(?otherEntities) = 2 || COUNT(?otherEntities)>2)
  ''',
  initNs = {"foaf":FOAF}
)


# Visualize the results
for r in g.query(q5):
  print(r.entities, r.numberOfKnownEntities)


