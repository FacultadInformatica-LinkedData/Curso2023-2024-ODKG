# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file
#
# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD, FOAF
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0/"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
NS = Namespace("http://somewhere#")


# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**
#
# %%
#RDFLib
print("TASK 7.1-RDFLib______________")
subclasses = set()
def get_subclasses(class_uri):
  for s, p, o in g.triples((None, RDFS.subClassOf, class_uri)):
    subclasses.add(s)
    get_subclasses(s)
get_subclasses(NS.LivingThing)
# Visualize the results
for subclass in subclasses:
  print(subclass)
  
print("TASK 7.1-SPARSQL______________")
#SPARQL
q1 = prepareQuery('''
  SELECT ?subClass WHERE { 
    ?subClass rdfs:subClassOf+ ns:LivingThing. 
    
  }
  ''',
  initNs = {"rdfs":RDFS, "ns":NS}
)
# Visualize the results
for r in g.query(q1):
  print(r.subClass)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 
# %%
#RDFlib
print("TASK 7.2-RDFLib______________")
individuals = set()
def is_subclass_of_person(class_uri):
  for s, p, o in g.triples((class_uri, RDFS.subClassOf, None)):
    if o == NS.Person or is_subclass_of_person(o):
      return True
  return False
for s, p, o in g.triples((None, RDF.type, None)):
  if o == NS.Person or is_subclass_of_person(o):
    individuals.add(s)
# Visualize the results
for individual in individuals:
  print(individual)

#SPARQL
print("TASK 7.2-SPARSQL______________")
q2 = prepareQuery('''
  SELECT DISTINCT ?individual WHERE { 
    ?individual rdf:type ?subClass. 
    ?subClass rdfs:subClassOf* ns:Person. #Included Person as subclass of itself
  }
  ''',
  initNs = {"rdfs":RDFS, "ns":NS}
)
# Visualize the results
for r in g.query(q2):
  print(r.individual)

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 
# %%
#RDFlib
print("TASK 7.3-RDFLib______________")
results = []
for s1, p1, o1 in g:
  for s2, p2, o2 in g.triples((s1, RDF.type, None)):
    if o2 == NS.Person or o2 == NS.Animal:
      results.append((str(s1), str(p1), str(o1)))
# Visualize the results
for (s,p,o) in results:
  print(s,p,o)

#SPARQL
print("TASK 7.3-SPARSQL______________")
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
  initNs = {"rdfs":RDFS, "ns":NS}
)
# Visualize the results
for r in g.query(q3):
  print(r.personOrAnimal, r.properties, r.value)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**
#
# %%
#RDFlib
print("TASK 7.4-RDFLib______________")
people_who_know_rocky = set()
rocky_uri = None
for s, p, o in g.triples((None, VCARD.Given, Literal("Rocky", datatype=XSD.string))):
  rocky_uri = s
def is_subclass_of_person(class_uri):
  for s, p, o in g.triples((class_uri, RDFS.subClassOf, None)):
    if o == NS.Person or is_subclass_of_person(o):
      return True
  return False
for s, p, o in g.triples((None, FOAF.knows, rocky_uri)):
  for _, _, t in g.triples((s, RDF.type, None)):
    if t == NS.Person or is_subclass_of_person(t):
      for _, _, name in g.triples((s, VCARD.Given, None)):
        people_who_know_rocky.add(name)
# Visualize the results
for name in people_who_know_rocky:
  print(name)
  
#SPARQL
print("TASK 7.4-SPARSQL______________")
q4= prepareQuery('''
   SELECT DISTINCT ?namePersonwhoKnowsRocky 
   WHERE {
      ?Rocky vcard:Given ?given.
      ?uriPersonwhoKnowsRocky foaf:knows ?Rocky.
      ?uriPersonwhoKnowsRocky vcard:Given ?namePersonwhoKnowsRocky.
      
      { ?uriPersonwhoKnowsRocky rdf:type ns:Person . }
      UNION
      { ?uriPersonwhoKnowsRocky rdf:type ?type .
        ?type rdfs:subClassOf* ns:Person . }
   }
  ''',
  initNs = { "vcard": VCARD.replace("#","/"), "rdfs":RDFS, "ns":NS, "foaf":FOAF, "rdf":RDF}
)
# Visualize the results
for r in g.query(q4, initBindings={'?given': Literal("Rocky", datatype=XSD.string)}):
  print(r.namePersonwhoKnowsRocky)

# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**
#
# %%
#RDFlib
print("TASK 7.5-RDFLib______________")
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

#SPARQL
print("TASK 7.5-SPARSQL______________")
q5= prepareQuery('''
  SELECT DISTINCT ?entities (COUNT(?otherEntities) as ?numberOfKnownEntities) WHERE 
  {
    ?entities foaf:knows ?otherEntities.
    FILTER(?entities != ?otherEntities).
  } GROUP BY ?entities
    HAVING (COUNT(?otherEntities) >= 2)
  ''',
  initNs = {"foaf":FOAF}
)
# Visualize the results
for r in g.query(q5):
  print('Entity:', r.entities, 'knows', r.numberOfKnownEntities, 'other entities')
  