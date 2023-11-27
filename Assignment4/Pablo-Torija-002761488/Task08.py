# %% [markdown]
# **Task 08: Completing missing data**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

# %% [markdown]
# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# %%
from rdflib import RDF
from rdflib.plugins.sparql import prepareQuery


data = Namespace('http://data.org#')
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

q1 = prepareQuery("""
    select ?person ?property ?value
    where {
        ?person rdf:type <http://data.org#person>.
        ?person ?property ?value
    }""",
)

for r in g1.query(q1):
 print(r)

for p1 in g1.subjects(RDF.type, data.person):
    p = [vcard.Given, vcard.Family, vcard.EMAIL]

    for property in p:
        if not (p1, property, None) in g1:
            o2 = g2.value(p1,property)
            if o2:
                g1.add((p1, property, o2))


print(g1.serialize(format="ttl"))