# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1chRGXGFvXqgRp9M9dEu0LfcadmOGFmCU

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

print('Grafo 1')
for s,p,o in g1:
  print(s,p,o)

print('Grafo 2')
for s,p,o in g2:
  print(s,p,o)

from rdflib.namespace import RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery

VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')

q1 = prepareQuery('''
SELECT ?person ?given ?family WHERE{
  ?person VCARD:Given ?given.
  ?person VCARD:Family ?family
}
''',
    initNs={'VCARD': VCARD}
)

graph1 = g1.query(q1)
graph2 = g2.query(q1)
for i in graph1:
  for j in graph2:
    if i[1] == j[1] and i[2] == j[2]:
      g3.add((i[0],OWL.sameAs,j[0]))
      break

for s,p,o in g3:
  print(s,p,o)