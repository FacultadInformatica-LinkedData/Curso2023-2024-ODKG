# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %% [markdown]
# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# %%
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")

q1 = prepareQuery('''
        SELECT ?subclass
        WHERE {
            ?subclass rdfs:subClassOf ns:Person
        }
    ''',
    initNs={
        'ns': ns,
        'rdfs': RDFS
    })

# Visualize the results
for r in g.query(q1):
    print(r)

# %%
for subclass in g.subjects(RDFS.subClassOf, ns.Person):
    print(subclass)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
q2 = prepareQuery('''
        SELECT ?individual
        WHERE {
            ?subclass rdfs:subClassOf* ns:Person .
            ?individual a ?subclass
        }
    ''',
    initNs={
        'ns': ns,
        'rdfs': RDFS
    })

# Visualize the results
for r in g.query(q2):
    print(r)

# %%
classes = [*g.subjects(RDFS.subClassOf, ns.Person), ns.Person]
for person_class in classes:
    for individual in g.subjects(RDF.type, person_class):
        print(individual)

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# %%
q3 = prepareQuery('''
        SELECT ?individual ?property ?value
        WHERE {
            ?subclass rdfs:subClassOf* ns:Person .
            ?individual a ?subclass .
            ?individual ?property ?value
        }
    ''',
    initNs={
        'ns': ns,
        'rdfs': RDFS
    })

# Visualize the results
for r in g.query(q3):
    print(r)

# %%
classes = [*g.subjects(RDFS.subClassOf, ns.Person), ns.Person]
for person_class in classes:
    for individual in g.subjects(RDF.type, person_class):
        for subject, prop, value in g.triples((individual, None, None)):
            print(subject, prop, value)


