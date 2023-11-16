# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0/"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %% [markdown]
# Using `SPARQL` on RDFLib
# 

# %%
# TO DO
#Creating the namespace object
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
# Binding the prefixes
g.bind('rdfs',RDFS)
g.bind('ns',ns)
g.bind('foaf',FOAF)
g.bind('rdf',RDF)
g.bind('vcard',VCARD)

# Define the SPARQL query
query_text = """    
    SELECT ?subclass WHERE {
        ?subclass rdfs:subClassOf* ns:LivingThing .
        
    }    
"""
#Prepare the query
query = prepareQuery(query_text,initNs = {"ns":ns,"rdfs":RDFS})

# Execute the query
# Visualize the results
for row in g.query(query):
    print(row)

# %% Using RDFlIB only
# TO DO
def get_subclasses(g, class_name,subclasses):
    """Return all the subclasses of a given class"""

    for s, p, o in g.triples((None, RDFS.subClassOf, class_name)):
        subclasses.append(s)
        get_subclasses(g, s,subclasses)
    return subclasses
    

# Get all the subclasses of LivingThing and its subclasses
subclasses = get_subclasses(g, ns.LivingThing,subclasses = list())
for s in subclasses:
    print(s)        

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %% [markdown]
# Using `SPARQL` on RDFLib

# %%
# TO DO
#Select all the individuals of type ns:Person and any of its subclasses

query_text = """
SELECT ?individual
WHERE {
    { ?individual rdf:type ns:Person . }
    UNION
    { ?individual rdf:type ?type .
      ?type rdfs:subClassOf* ns:Person . }
}

"""
query = prepareQuery(query_text,initNs={'ns':ns,'rdf':RDF,'rdfs':RDFS})

# Execute the query
#Visualize the results
for row in g.query(query):
    print(f"Individual: {row[0]} ")

# %% Using RDFlIB only


# Get all the individuals of Person and its subclasses
subclasses = get_subclasses(g, ns.Person,subclasses = [ns.Person])
for s in subclasses:
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
        print(s1)
# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %% [markdown]
# Using `SPARQL` on `RDFLib`

# %%
# TO DO

# Define query
query_text = """
    SELECT ?individual ?property ?value
    WHERE {
        ?individual rdf:type ?class .
        ?individual ?property ?value .
        {?individual rdf:type ns:Person .}
        UNION
        {?individual rdf:type ns:Animal .}
    }
"""
query = prepareQuery(query_text, initNs={'ns':ns,'rdf':RDF})

# Execute the query
# Visualize the results
for row in g.query(query):
    print(f'Individual: {row[0]}, Property: {row[1]}, Value: {row[2]}')



# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %% [markdown]
# Using `SPARQL` on `RDFLib`

# %%
# TO DO

# Define the SPARQL query
query_text = """
    SELECT ?Subject ?name WHERE {
    ?Rocky vcard:Given ?given.
    ?Subject foaf:knows ?Rocky.
    { ?Subject rdf:type ns:Person . }
    UNION
    { ?Subject rdf:type ?type .
      ?type rdfs:subClassOf ns:Person . }
      ?Subject vcard:Given ?name.
   }
"""


query = prepareQuery(query_text,initNs={'vcard':VCARD,'ns':ns,'rdf':RDF,'foaf':FOAF})

# Execute the query
# Visualize the results
for row in g.query(query,initBindings = {'?given' : Literal('Rocky', datatype=XSD.string)}):
  print(row[1])


# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %% [markdown]
# Using `SPARQL` on `RDFLib`

# %%
query_text = """
    SELECT ?ent1 (COUNT(?ent2) AS ?c)
    WHERE {
        ?ent1 foaf:knows ?ent2 .
    }
    GROUP BY ?ent1
    HAVING (COUNT(?ent2) >= 2)
"""

# Execute the query and print entities who know at least two other entities
results = g.query(query_text,initNs={'foaf':FOAF})
for row in results:
    print(f'Entity: {row[0]}, knows {row[1]} other entities')

# %% [markdown]
# Using `RDFLib` only

# %%
from collections import Counter
# TO DO

# Create a counter object
knows_counter = Counter()

# Each time we find an entity that knows another entity, 
# increase + 1 its counter
for s, p, o in g.triples((None, FOAF.knows, None)):
    knows_counter[s] += 1

# Print entities who know at least two other entities
for entity, count in knows_counter.items():
    if count >= 2:
        print(f'Entity: {entity} knows {count} other entities')


