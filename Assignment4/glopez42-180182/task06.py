"""Task06.ipynb

**Task 06: Modifying RDF(s)**
"""
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.namespace_manager.bind('ns', ns, override=False)
g.namespace_manager.bind('vcard', VCARD, override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**"""

print("**TASK 6.1**")
g.add((ns.University, RDF.type, RDFS.Class))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

print("**TASK 6.2**")
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

print("**TASK 6.3**")
g.add((ns.JaneSmith, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""

print("**TASK 6.4**")
g.add((ns.JaneSmith, VCARD.EMAIL, Literal("jane.smith@mail.com")))
g.add((ns.JaneSmith, VCARD.FN, Literal("Jane Smith")))
g.add((ns.JaneSmith, VCARD.Given, Literal("Jane")))
g.add((ns.JaneSmith, VCARD.Family, Literal("Smith")))

# Visualize the results
print(g.serialize(format="ttl"))


"""**TASK 6.5: Add UPM as the university where John Smith works**"""

print("**TASK 6.5**")
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, ns.worksAt, ns.UPM))

# Visualize the results
print(g.serialize(format="ttl"))

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""

print("**TASK 6.6**")

from rdflib import FOAF
g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))

# Visualize the results
print(g.serialize(format="ttl"))
