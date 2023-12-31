# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14ywho9CbE7kuGvpxFhXTyFm91vcIvhFO

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

from rdflib.namespace import OWL, RDFS
from rdflib.plugins.sparql import prepareQuery
ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# Datos del primer grafo
q1 = prepareQuery('''
    SELECT ?person ?given ?family
    WHERE
    {
    ?person rdf:type ns1:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
    }
  ''',
    initNs = { "ns1": ns1,"vcard":vcard}
)
results = g1.query(q1)

# Datos del segundo grafo
q2 = prepareQuery('''
SELECT ?person ?given ?family WHERE {
    ?person rdf:type ns2:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
}
  ''',
    initNs = { "ns2": ns2,"vcard":vcard}
)
results2 = g2.query(q2)

# Establecer propiedad OWL:sameAs
for r1 in results:
    for r2 in results2:
        if r1.given == r2.given and r1.family == r2.family:
            g3.add((r1.person, OWL.sameAs, r2.person))

# Imprimir grafo 3
for s,p,o in g3:
    print(s,p,o)