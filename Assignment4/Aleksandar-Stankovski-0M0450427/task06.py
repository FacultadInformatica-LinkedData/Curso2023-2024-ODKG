
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
# Visualize the results
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
# Visualize the results
g.add((ns.Research, RDFS.subClassOf, ns.Person))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

# TO DO
# Visualize the results
fullName = Literal("Jane Smith")
janeURI = ns.JaneSmith
resource = (janeURI, RDF.type, ns.Researcher)
g.add(resource)
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""

# TO DO
# Visualize the results
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
resource = (janeURI, VCARD.Email, Literal("smith.jane@gmail.com"))
g.add(resource)
resource = (janeURI, VCARD.FN, Literal("Jane Smith"))
g.add(resource)
resource = (janeURI, VCARD.Given, Literal("Sanchez"))
g.add(resource)
resource = (janeURI, VCARD.Family, Literal("Gomez"))
g.add(resource)
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""

# TO DO
# Visualize the results
upmURI = ns.UPM
resource = (upmURI, RDF.type, ns.University)

g.add(resource)
JohnSmithURI = ns.JohnSmith
g.add((ns.worksAt, RDF.type, RDF.Property))
resource = (JohnSmithURI, ns.worksAt, ns.UPM)
g.add(resource)

for s, p, o in g:
  print(s,p,o)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""

# TO DO
# Visualize the results

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
resource = (JohnSmithURI, FOAF.knows, janeURI)
g.add(resource)

for s, p, o in g:
  print(s,p,o)