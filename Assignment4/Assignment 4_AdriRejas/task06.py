# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L-YB4gM-tQYPSJEs_2MZjx6aQHRresnk

**Task 06: Modifying RDF(s)**

**Assignment 4** \
Adrián Rejas Llamera
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
# Defining a namespace and storing its URI in the variable ns
ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class)) # New class created
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

# TO DO
jane_smith = ns.JaneSmith
g.add((jane_smith, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""

# TO DO
#Defining VCARD space
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

g.add((jane_smith, vcard.FN, Literal("Jane Smith")))
g.add((jane_smith, vcard.Given, Literal("Jane")))
g.add((jane_smith, vcard.Family, Literal("Smith")))
g.add((jane_smith, vcard.EMAIL, Literal("jane.smith@example.com")))
# Visualize the results
for s, p, o in g:
  print(s, p, o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""

# TO DO
# Creating an individual named "UPM" representing the university
upm = ns.UPM
g.add((upm, RDF.type, ns.University))
g.add((upm, vcard.name, Literal("Universidad Politécnica de Madrid")))
# Associating "John Smith" with the university "UPM"
john_smith = ns.john_smith
g.add((john_smith, vcard.work, upm))
# Visualize the results
for s, p, o in g:
  print(s, p, o)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""

# TO DO
from rdflib import FOAF

#Defining FOAF vocabulary
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# Establishing the "knows" relationship between "John Smith" and "Jane Smith"
g.add((john_smith, FOAF.knows, jane_smith))

# Visualize the results
for s, p, o in g:
  print(s, p, o)
