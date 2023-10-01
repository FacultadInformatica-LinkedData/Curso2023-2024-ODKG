# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17-APxnStNCFdK3NgHdNabdyMME_gX_ay

**Task 07: Querying RDF(s)**
"""

#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")
from rdflib.plugins.sparql import prepareQuery

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""
print("TASK 7.1")
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
print("Printeamos los resultados obtenidos con rdfslib")
for s,p,o in g.triples((None,rdfs.subClassOf,ns.Person)):
  print(s)
# Visualize the results

q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf ns:Person
  } 
  ''',
  initNs = { "vcard": vcard,"rdfs":rdfs,"ns":ns}
)
print("Printeamos los resultados obtenidos con sparql")
for r in g.query(q1):
  print(r.Subject)

#for r in g.query(q1):
#  print(r)
print("------------------------------------------------------------------------------------------------------------------------------------------")
"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""
print("TASK 7.2")
print("Printeamos los resultados obtenidos con rdfslib")
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  print(s)

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
q2 = prepareQuery('''
  SELECT DISTINCT ?s
  WHERE { 
    {
      ?s rdf:type ns:Person. 
    }
    UNION {
      ?p rdfs:subClassOf* ns:Person.
            ?s rdf:type ?p
    }
  }
  ''',
                  initNs={"rdfs": RDFS, "rdf": RDF, "ns": ns}
                  )
for r in g.query(q2):
  print(r.s)
# Visualize the results
print("------------------------------------------------------------------------------------------------------------------------------------------")
"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""
print("TASK 7.3")
print("Printeamos los resultados obtenidos con rdfslib")
for s1,p1,o1 in g.triples((None,RDF.type,ns.Person)):
  for s2,p2,o2 in g.triples((s1,None,None)):
    print(s2,p2,o2)


from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
q1 = prepareQuery('''
  SELECT ?Subject ?prop ?ob WHERE { 
 {
      ?s rdf:type ns:Person. 
    }
    UNION {
      ?p rdfs:subClassOf* ns:Person.
            ?s rdf:type ?p
    }
    ?Subject ?prop ?ob.
  } 
  ''',
  initNs = { "vcard": vcard,"rdfs":rdfs,"ns":ns}
)
print("Printeamos los resultados obtenidos con sparql")
for r in g.query(q1):
  print(r.Subject,r.prop,r.ob)
# Visualize the results
