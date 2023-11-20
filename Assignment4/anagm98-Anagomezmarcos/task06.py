# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vgrIYGF8YBa-3FwCMSVrnwOfeA6Iu8UI

**Task 06: Modifying RDF(s)**
"""


!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**

"""

# TO DO
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
g.add((ns.Researcher, RDF.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

# TO DO
idPersona = URIRef(ns["JaneSmith"])
g.add((idPersona, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""

# TO DO
vcard = NameSpace("http://www.w3.org/2001/vcard-rdf/3.0#")

fullName = Literal("Jane Smith")
given = Literal("Smith")
family = Literal("Jane")

g.add((idPersona, vcard.FN, fullName))
g.add((idPersona, vcard.Given, given))
g.add((idPersona, vcard.Family, family))

# Visualize the results
for s, p, o in g.triples((ns.JaneSmith, None, None)):
  print(s,p,o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""

# TO DO
idUniversidad = URIRef(ns["UPM"])
idPersona2 = URIRef(ns["JohnSmith"])

g.add((idUniversidad, RDF.type, ns.University))
g.add((idUniversidad, vcard.FN, Literal("UPM")))
g.add((idPersona2, vcard.Work, idUniversidad))
# Visualize the results
for s, p, o in g.triples((ns.JohnSmith, None, None)):
  print(s,p,o)
for s, p, o in g.triples((ns.UPM, None, None)):
  print(s,p,o)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""

# TO DO
idJane = URIRef(ns["JaneSmith"])
idJohn = URIRef(ns["JohnSmith"])

g.add((idJohn, FOAF.knows, idJane))
# Visualize the results
for s, p, o in g.triples((idJohnSmith, FOAF.knows, None)):
  print(s, p, o)
