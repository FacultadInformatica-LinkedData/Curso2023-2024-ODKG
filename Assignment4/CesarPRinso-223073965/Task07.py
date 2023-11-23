# -*- coding: utf-8 -*-

# Instalar la biblioteca rdflib si aún no está instalada
# !pip install rdflib

# URL del almacenamiento en GitHub
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# Leer el archivo RDF
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

# Crear el grafo RDF
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/rdf/example6.rdf", format="xml")

# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**
print("TASK 7.1: List all subclasses of 'LivingThing' with RDFLib and SPARQL")
print("RDFLib:")
for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
    if (o, RDFS.subClassOf, ns.LivingThing) in g:
        print(o)

print("SPARQL:")
q1 = """
    SELECT ?subclass
    WHERE {
        ?subclass rdf:type/rdfs:subClassOf* ns:LivingThing .
    }
"""
for row in g.query(q1):
    print(row.subclass)

# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
print("\nTASK 7.2: List all individuals of 'Person' with RDFLib and SPARQL")
print("RDFLib:")
for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
    if (o, RDFS.subClassOf, ns.Person) in g:
        for individual in g.subjects(RDF.type, o):
            print(individual)

print("SPARQL:")
q2 = """
    SELECT ?individual
    WHERE {
        ?individual rdf:type/rdfs:subClassOf* ns:Person .
    }
"""
for row in g.query(q2):
    print(row.individual)

# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
print(
    "\nTASK 7.3: List all individuals of 'Person' or 'Animal' and all their properties including their class with RDFLib and SPARQL")
print("RDFLib:")
for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
    if (o, RDFS.subClassOf, ns.Person) in g or (o, RDFS.subClassOf, ns.Animal) in g:
        for individual in g.subjects(RDF.type, o):
            for p, o in g.predicate_objects(individual):
                print(f"{individual} {p} {o}")

print("SPARQL:")
q3 = """
    SELECT ?individual ?property ?value
    WHERE {
        {
            ?individual rdf:type ns:Person .
        } UNION {
            ?individual rdf:type ns:Animal .
        }
        ?individual ?property ?value .
    }
"""
for row in g.query(q3):
    print(row.individual, row.property, row.value)

# **TASK 7.4:  List the name of the persons who know Rocky**
print("\nTASK 7.4: List the name of the persons who know Rocky")
print("RDFLib:")
for s, p, o in g.triples((None, ns.knows, ns.Rocky)):
    if (s, RDF.type, ns.Person) in g:
        for name in g.objects(s, VCARD.FN):
            print(name)

print("SPARQL:")
q4 = """
    SELECT ?name
    WHERE {
        ?person ns:knows ns:Rocky .
        ?person rdf:type ns:Person .
        ?person vcard:FN ?name .
    }
"""
for row in g.query(q4):
    print(row.name)

# **Task 7.5: List the entities who know at least two other entities in the graph**
print("\nTask 7.5: List the entities who know at least two other entities in the graph")
print("RDFLib:")
knows_count = {}
for s, p, o in g.triples((None, ns.knows, None)):
    if s not in knows_count:
        knows_count[s] = 1
    else:
        knows_count[s] += 1

for entity, count in knows_count.items():
    if count >= 2:
        print(entity)

print("SPARQL:")
q5 = """
    SELECT ?entity
    WHERE {
        {
            SELECT ?entity (COUNT(?known) as ?count)
            WHERE {
                ?entity ns:knows ?known .
            }
            GROUP BY ?entity
        }
        FILTER (?count >= 2)
    }
"""
for row in g.query(q5):
    print(row.entity)
