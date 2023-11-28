# %% [markdown]
# **Task 09: Data linking**

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

# %% [markdown]
# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# %%
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import Namespace,RDF

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
three = Namespace("http://data.three.org#")
owl = Namespace("http://www.w3.org/2002/07/owl#")

for i in g1.subjects(RDF.type, None):
    n = g1.value(i, vcard.Given)
    f = g1.value(i, vcard.Family)

    for i2 in g2.subjects(RDF.type, None):
        n2 = g2.value(i2, vcard.Given)
        f2 = g2.value(i2, vcard.Family)

        if n == n2 and f == f2:
            g3.add((i,owl.sameAs,i2))

print(g3.serialize(format="ttl"))