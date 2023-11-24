
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF
g = Graph()
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

def get_subclasses(class_name):
    all_subclasses = []
    for s, _, _ in g.triples((None, RDFS.subClassOf, class_name)):
        all_subclasses.append(s)
        all_subclasses.extend(get_subclasses(s))

    return all_subclasses

all_subclasses = get_subclasses(ns.LivingThing)
for s in all_subclasses:
    print(s)

print('--------------------------------')

q1 = """SELECT ?subClass
WHERE {
  ?subClass rdfs:subClassOf/rdfs:subClassOf* <http://somewhere#LivingThing> .
}"""

for r in g.query(q1):
 print(r[0])

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

all_persons = [] # To be reused later
for s, _, _ in g.triples((None, RDF.type, ns.Person)):
    print(s)
    all_persons.append(s)

all_subclasses = get_subclasses(ns.Person)
for subclass in all_subclasses:
    for individual in g.triples((None, RDF.type, subclass)):
        print(individual[0])
        all_persons.append(individual[0])

print('--------------------------------')

q = """
SELECT ?x
    WHERE {
        ?x rdf:type/rdfs:subClassOf* ns:Person.
    }
"""

for r in g.query(q):
 print(r[0])

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

all_properties = []
for class_name in [ns.Person, ns.Animal]:
    for s, _, _ in g.triples((None, RDF.type, class_name)):
        p = [p for _, p, _ in g.triples((s, None, None))]
        all_properties.append((s, class_name, p))

for properties in all_properties:
    print(f"Properties for individual: {properties[0]}")
    print(properties)

print('--------------------------------')

q = """
PREFIX ns: <http://somewhere#>
SELECT ?x ?property ?value
WHERE {
    {
        ?x rdf:type ns:Person .
        ?x ?property ?value .
    } UNION {
        ?x rdf:type ns:Animal .
        ?x ?property ?value .
    }
}
"""

for r in g.query(q):
    print(r[1])

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

for person in all_persons: # Reusing the list from before
    for s, _, _ in g.triples((person, FOAF.knows, ns.RockySmith)):
        print(s)

print('--------------------------------')

q = """
SELECT ?x
    WHERE {
        ?x rdf:type/rdfs:subClassOf* ns:Person.
        ?x foaf:knows ns:RockySmith.
    }
"""

for r in g.query(q):
    print(r[0])

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

knows_count = {}
for s, _, _ in g.triples((None, FOAF.knows, None)):
    if not s in knows_count.keys():
        knows_count[s] = 0
    knows_count[s] += 1

# Filter knows_count to only include entities that know more than 2 people
knowers = {k: v for k, v in knows_count.items() if v >= 2}
for k in knowers.keys():
    print(k)

print('--------------------------------')

q1 = """SELECT ?x
WHERE {
  ?x <http://xmlns.com/foaf/0.1/knows> ?entity1 .
  ?x <http://xmlns.com/foaf/0.1/knows> ?entity2 .
  FILTER (?entity1 != ?entity2)
} GROUP BY ?x HAVING ((COUNT(DISTINCT ?entity1) + COUNT(DISTINCT ?entity2)) >= 2)"""

for r in g.query(q1):
    print(r[0])