# -*- coding: utf-8 -*-

# Instalar la biblioteca rdflib si aún no está instalada
# !pip install rdflib

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, URIRef

g1 = Graph()
g2 = Graph()

g1.parse(github_storage + "resources/data01.rdf", format="xml")
g2.parse(github_storage + "resources/data02.rdf", format="xml")

ns = Namespace("http://data.org#")

q1 = """
    SELECT ?person
    WHERE {
        ?person rdf:type ns:Person .
    }
"""

for row in g1.query(q1):
    person_uri = row.person

    if (person_uri, ns.Given, None) not in g1 or (person_uri, ns.Family, None) not in g1 or (
    person_uri, ns.EMAIL, None) not in g1:
        if (person_uri, RDF.type, ns.Person) in g2:
            given_name = g2.value(person_uri, ns.Given, any=False)
            family_name = g2.value(person_uri, ns.Family, any=False)
            email = g2.value(person_uri, ns.EMAIL, any=False)

            if given_name:
                g1.add((person_uri, ns.Given, given_name))
            if family_name:
                g1.add((person_uri, ns.Family, family_name))
            if email:
                g1.add((person_uri, ns.EMAIL, email))

print("Grafo 1 después de completar los datos:")
for s, p, o in g1:
    print(s, p, o)
