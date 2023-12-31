# -*- coding: utf-8 -*-
"""SparqlQueries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rQmQf_p07qnvdy-u5JCKPBDY5lav8inK
"""

!pip install rdflib

g = Graph()
g.parse("RDF_healthCenters.ttl", format="ttl")

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

foaf = Namespace("http://xmlns.com/foaf/0.1/")
RDF = ("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
vcard = ("http://www.w3.org/2001/vcard-rdf/3.0#")
vocab = Namespace ("http://healthcentersmadrid.es/locations/ontology/ont#")

print(g)

from rdflib.plugins.sparql import prepareQuery

#List all entities (nodes of the RDF graph) by name in alphabetical order.
q1 = prepareQuery('''
  SELECT ?name
  WHERE {
    ?entity rdf:type vocab:HealthCenter.
    ?entity vocab:name ?name .
  }
  ORDER BY ?name
  ''',
  initNs = { "rdf": RDF, "vocab":vocab}
)

# Visualize the results
for s in g.query(q1):
  print(s.name)

from rdflib.plugins.sparql import prepareQuery

#List all entities fot a specific neighbourhood (PROSPERIDAD)
q2 = prepareQuery('''
  SELECT ?entity ?name
  WHERE {
    ?entity rdf:type vocab:HealthCenter.
    ?entity vocab:name ?name.
    ?entity vocab:Location ?Location.
    ?Location vocab:Address ?Address.
    ?Address vocab:neighbourhood "PROSPERIDAD".
  }
  ''',
  initNs = { "rdf": RDF, "vocab":vocab}
)

# Visualize the results
for s in g.query(q2):
  print(s.name)

from rdflib.plugins.sparql import prepareQuery
foaf = Namespace("http://xmlns.com/foaf/0.1/")

#Retrieve the name of the health centers of a certain type
q3 = prepareQuery('''
SELECT ?name
WHERE {
    ?entity rdf:type vocab:HealthCenter.
    ?entity vocab:name ?name .
    ?entity vocab:hasType "/contenido/entidadesYorganismos/CentrosAtencionMedica/CentrosSalud".
}
''',
  initNs = { "rdf": RDF, "vocab":vocab}
)

# Visualize the results
for s in g.query(q3):
    print(s.name)