# %% [markdown]
# **Task 09: Data linking**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

print("G1--------------------------------------------------------------------------------------")
for s,p,o in g1:
    print(s,p,o)
print("G2--------------------------------------------------------------------------------------")
for s,p,o in g2:
    print(s,p,o)

# %% [markdown]
# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# %%
from rdflib.namespace import OWL, RDFS
from rdflib.plugins.sparql import prepareQuery

# Crear el tercer grafo
g3 = Graph()

# Definir las URIs que se utilizarán en las consultas SPARQL
ns = dict(
    rdf=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    vcard=URIRef("http://www.w3.org/2001/vcard-rdf/3.0#"),
    xsd=URIRef("http://www.w3.org/2001/XMLSchema#"),
    data1=URIRef("http://data.three.org#"),
    data2=URIRef("http://data.four.org#"),
    owl=OWL,
)

# Consulta SPARQL para obtener todos los individuos y sus apodos y apellidos
q1 = prepareQuery('''
SELECT ?person ?given ?family WHERE {
    ?person rdf:type data1:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
}
''', initNs=ns)

q2 = prepareQuery('''
SELECT ?person ?given ?family WHERE {
    ?person rdf:type data2:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
}
''', initNs=ns)

# Ejecutar la consulta en ambos grafos
results1 = g1.query(q1)
results2 = g2.query(q2)


# Para cada individuo en el primer grafo
for r1 in results1:
    for r2 in results2:
        if r1.given == r2.given and r1.family == r2.family:           
            g3.add((r1.person, OWL.sameAs, r2.person))

print("G3--------------------------------------------------------------------------------------")
for s,p,o in g3:
    print(s,p,o)



