
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

Task: List all the elements of the Person class in the first graph (data01.rdf) and complete the fields (given name, family name and email) that may be missing with the data from the second graph (data02.rdf). You can use SPARQL queries or iterate the graph, or both.
"""

# Manual Inspection & Analysis

print("Listing all elements from class Person")

# Find all elements from class Person
persons_query = """SELECT ?x
WHERE {
  ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.org#Person> .
}"""

for r in g1.query(persons_query):
 print(r[0])
print()

print("Listing all properties of the elements from class Person")

# Find all properties of the elements from class Person
person_properties_query = """SELECT ?x ?y ?z
WHERE {
  ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.org#Person> .
  ?x ?y ?z .
  FILTER (?y != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
}"""

for r in g1.query(person_properties_query):
 print(r[0], r[1], r[2])
print()

# Conclusions
print("As we can see some properties are missing like:")
print("Sara Jones: Given name, Family Name and Email")
print("John Smith: Family Name")
print("John Doe: Given Name")
print("Harry Potter: Email")

# Initialize lists with persons and properties
persons = [x[0] for x in g1.query(persons_query)]
properties = ["http://www.w3.org/2001/vcard-rdf/3.0#Given", "http://www.w3.org/2001/vcard-rdf/3.0#Family", "http://www.w3.org/2001/vcard-rdf/3.0#EMAIL"]

# Iterate lists to check if the property is missing
# If it is missing, try to find it in g2 and add it to g1
for person in persons:
  for property in properties:
    for s, p, o in g2.triples((URIRef(person), URIRef(property), None)):
          g1.add((s, p, o))

# Check if the properties have been added

print("Listing all properties of the elements from class Person")
person_properties_query = """SELECT ?x ?y ?z
WHERE {
  ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://data.org#Person> .
  ?x ?y ?z .
  FILTER (?y != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
}"""
for r in g1.query(person_properties_query):
 print(r[0], r[1], r[2])
print()

print("We can see that all properties are now present in g1")