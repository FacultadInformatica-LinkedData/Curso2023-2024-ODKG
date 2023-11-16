# -*- coding: utf-8 -*-
"""Task06.ipynb**Task 06: Modifying RDF(s)**"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.namespace_manager.bind('ns', ns, override=False)
g.namespace_manager.bind('vcard', vcard, override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""
g.add((ns.Researcher, RDF.type, RDFS.Class))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**"""
g.add((ns.University, RDF.type, RDFS.Class))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""
JaneSmith = ns.JaneSmith
g.add((JaneSmith, RDF.type, ns.Researcher))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""
from rdflib import URIRef
g.add((JaneSmith, vcard.EMAIL, URIRef("mailto:jane.smith@upm.es")))
g.add((JaneSmith, vcard.FN, Literal("Jane Smith")))
g.add((JaneSmith, vcard.Given, Literal("Jane")))
g.add((JaneSmith, vcard.Family, Literal("Smith")))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""
JohnSmith = ns.JohnSmith
UPM = ns.UPM
g.add((UPM, RDF.type, ns.University))
g.add((ns.worksAt, RDF.type, RDF.Property))
g.add((JohnSmith, ns.worksAt, UPM))

# Visualize the results
# for s, p, o in g:
#   print(s,p,o)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""
# Did you mean 'John'?
from rdflib import FOAF
g.add((JohnSmith, FOAF.knows, JaneSmith))

# Visualize the results
for s, p, o in g:
  print(s,p,o)
