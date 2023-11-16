#%% md
# **Task 07: Querying RDF(s)**
#%%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"
#%% md
# First let's read the RDF file
#%%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")
#%% md
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**
#%% md
# SPARQL version
#%%
from rdflib.plugins.sparql import prepareQuery
NS = Namespace("http://somewhere#")

q1 = prepareQuery('''
    SELECT ?subclass WHERE {
      ?subclass rdfs:subClassOf* ns:LivingThing.
    }
    ''',
    initNs = {'rdfs':RDFS, 'ns':NS}
)

for r in g.query(q1):
    print(r.subclass)
#%% md
# 
#%% md
# For the RDFLib version we need to define a auxiliar function for the recursion
#%%
def get_subclasses(graph, parent_class):
    subclasses_list = []
    for s, _, _ in graph.triples((None, RDFS.subClassOf, parent_class)):
        subclasses_list += [s]
        subclasses_list += get_subclasses(graph, s)
        
    return subclasses_list
#%%
subclasses_list = [NS.LivingThing] + get_subclasses(g, NS.LivingThing)
print(*subclasses_list, sep="\n")
#%% md
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 
#%% md
# SPARQL version
#%%
q2 = prepareQuery('''
    SELECT ?individual WHERE {
        ?individual rdf:type/rdfs:subClassOf* ns:Person.
    }
    ''',
    initNs={'rdf': RDF, 'rdfs': RDFS, 'ns': NS}
)

for r in g.query(q2):
    print(r.individual)
#%% md
# RDFLib version
#%%
person_subclasses = [NS.Person] + get_subclasses(g, NS.Person)
for subclass in person_subclasses:
    for s, _, _ in g.triples((None, RDF.type, subclass)):
        print(s)
#%% md
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 
#%% md
# SPARQL version
#%%
q3 = prepareQuery('''
  SELECT ?individual ?thing ?prop ?clas WHERE {
      ?individual rdf:type ?thing.
      ?individual ?prop ?clas
      FILTER(?thing = ns:Person || ?thing = ns:Animal)
  }
  ''',
  initNs = {'ns': NS , 'rdf': RDF}
)

for r in g.query(q3):
    print(r.individual, r.thing, r.prop, r.clas)
#%% md
# RDFLib version
#%%
for thing in [NS.Animal, NS.Person]:
    for s1, p1, o1 in g.triples((None, RDF.type, thing)):
        for s2, p2, o2 in g.triples((s1, None, None)):
            print(s2, thing, p2, o2)
#%% md
# **TASK 7.4:  List the name of the persons who know Rocky**
#%%
# TO DO
# Visualize the results
from rdflib.namespace import FOAF

VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q4 = prepareQuery('''
    SELECT DISTINCT ?name
    WHERE {
       ?person foaf:knows ns:RockySmith .
       ?person vcard:FN ?name .
    }
    ''',
    initNs = {'ns': NS, 'foaf': FOAF, 'vcard': VCARD}
)

for r in g.query(q4):
    print(r. name)
#%% md
# **Task 7.5: List the entities who know at least two other entities in the graph**
#%%
# TO DO
# Visualize the results
q5 = prepareQuery('''
  SELECT DISTINCT ?entity  WHERE
  {
    ?entity foaf:knows ?person.
    FILTER(?entity != ?person).
  }
  GROUP BY ?entity
  HAVING (COUNT(DISTINCT ?person) >= 2)
  ''',
  initNs = { 'foaf': FOAF }
)

for r in g.query(q5):
    print(r.entity)