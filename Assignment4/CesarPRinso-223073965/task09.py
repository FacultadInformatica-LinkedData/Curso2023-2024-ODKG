# -*- coding: utf-8 -*-

# Instalar la biblioteca rdflib si aún no está instalada
# !pip install rdflib

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4/"

from rdflib import Graph, Namespace, Literal, RDF, OWL

g1 = Graph()
g2 = Graph()
g3 = Graph()

g1.parse(github_storage + "resources/data03.rdf", format="xml")
g2.parse(github_storage + "resources/data04.rdf", format="xml")

ns = Namespace("http://data.org#")

query = """
    SELECT ?individual1 ?individual2
    WHERE {
        ?individual1 rdf:type ns:Person .
        ?individual2 rdf:type ns:Person .
        ?individual1 ns:Given ?given1 .
        ?individual2 ns:Given ?given2 .
        ?individual1 ns:Family ?family1 .
        ?individual2 ns:Family ?family2 .
        FILTER (?given1 = ?given2 && ?family1 = ?family2 && ?individual1 != ?individual2)
    }
"""


for row1 in g1.query(query):
    for row2 in g2.query(query):
        if row1.individual1 == row2.individual2 and row1.individual2 == row2.individual1:
            g3.add((row1.individual1, OWL.sameAs, row1.individual2))

print("Grafo 3 después de enlazar individuos:")
for s, p, o in g3:
    print(s, p, o)
