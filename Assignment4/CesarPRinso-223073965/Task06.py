# -*- coding: utf-8 -*-

# Instalar la biblioteca rdflib si aún no está instalada
# !pip install rdflib

# URL del almacenamiento en GitHub
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# Leer el archivo RDF como se muestra en clase
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

# Crear el grafo RDF
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
    print(s, p, o)

# **TASK 6.1: Create a new class named "University"**
ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))

# Visualize the results
for s, p, o in g:
    print(s, p, o)

# **TASK 6.2: Add "Researcher" as a subclass of "Person"**
g.add((ns.Researcher, RDF.type, RDFS.Class))
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

# Visualize the results
for s, p, o in g:
    print(s, p, o)

# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**
g.add((ns.JaneSmith, RDF.type, ns.Researcher))

# Visualizar los resultados
for s, p, o in g:
    print(s, p, o)

# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.add((ns.JaneSmith, VCARD.EMAIL, Literal('jane.smith@example.com', datatype=RDF.XMLLiteral)))
g.add((ns.JaneSmith, VCARD.FN, Literal('Jane Smith', datatype=RDF.XMLLiteral)))
g.add((ns.JaneSmith, VCARD.Given, Literal('Jane', datatype=RDF.XMLLiteral)))
g.add((ns.JaneSmith, VCARD.Family, Literal('Smith', datatype=RDF.XMLLiteral)))

# Visualize the results
for s, p, o in g.triples((ns.JaneSmith, None, None)):
    print(s, p, o)

# **TASK 6.5: Add UPM as the university where John Smith works**
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, ns.Work, ns.UPM))

# Visualize the results
for s, p, o in g.triples((None, None, ns.UPM)):
    print(s, p, o)

# **Task 6.6: Add that John knows Jane using the FOAF vocabulary**
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))

# Visualize the results
for s, p, o in g.triples((ns.JohnSmith, FOAF.knows, None)):
    print(s, p, o)
