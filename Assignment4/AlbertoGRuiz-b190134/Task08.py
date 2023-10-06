# %% [markdown]
# **Task 08: Completing missing data**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

print("G1--------------------------------------------------------------------------------------")
for s,p,o in g1:
    print(s,p,o)
print("G2--------------------------------------------------------------------------------------")
for s,p,o in g2:
    print(s,p,o)

# %% [markdown]
# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# %%
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF

# Definir las URIs que se utilizarán en las consultas SPARQL
ns = dict(
    rdf=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    vcard=URIRef("http://www.w3.org/2001/vcard-rdf/3.0#"),
    xsd=URIRef("http://www.w3.org/2001/XMLSchema#"),
    data=URIRef("http://data.org#"),
)

# Consulta SPARQL para obtener todos los elementos de la clase Person
q1 = prepareQuery('''
  SELECT ?s WHERE {
    ?s rdf:type data:Person .
}
  ''',
  initNs = { "rdf": ns["rdf"], "data": ns["data"]}
)

# Ejecutar la consulta en el primer grafo
persons = g1.query(q1)

# Para cada persona, completar los campos faltantes con los datos del segundo grafo
for person in persons:
    person_uri = person[0]  
    for field in ["Given", "Family", "EMAIL"]:
        predicate_uri = URIRef(ns["vcard"] + field)
        if not any((s, p, o) in g1 for s, p, o in g1.triples((person_uri, predicate_uri, None))):
            q2 = f"""
            SELECT ?o WHERE {{
                {person_uri.n3()} vcard:{field} ?o .
            }}
            """
            results = g2.query(q2, initNs=ns)
            for result in results:
                # Añadir el campo al primer grafo
                g1.add((person_uri, predicate_uri, result[0]))

# Imprimir los resultados
q3 = prepareQuery('''
  SELECT ?person ?given ?family ?email
  WHERE {
    ?person rdf:type data:Person .
    ?person vcard:Given ?given .
    ?person vcard:Family ?family .
    ?person vcard:EMAIL ?email .
  }
  ''',
  initNs=ns
)
print("Results---------------------")
results = g1.query(q3)
for row in results:
    print(f"Person: "+row.person)
    print(f"Given:  "+row.given)
    print(f"Family: "+row.family)
    print(f"EMAIL:  "+row.email)
    print("---------------------")



