# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19qp2dB19X130URiaXqVDd0Xau6VgTNSD

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

print("RDFLib: ")

def get_subclasses(graph, class_p):
    subclasses = set()

    for subClass, _, _ in graph.triples((None, RDFS.subClassOf, class_p)):
        subclasses.add(subClass)
        # Recursively get subclasses of the current subclass
        subclasses |= get_subclasses(graph, subClass)

    return subclasses

# Get subclasses of "LivingThing"
living_thing_subclasses = get_subclasses(g, ns.LivingThing)

# Print the result
for subclass in living_thing_subclasses:
    print(subclass)

print("SPARQL: ")

q1 = prepareQuery(
        """
            SELECT ?subClass
            WHERE{
                ?subClass rdfs:subClassOf* ns:LivingThing .
            }
        """,
        initNs = {"rdfs":RDFS, "ns":ns})

for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")

print("RDFLib:")
for i, _, _ in g.triples((None, RDF.type, ns.Person)):
    print(i)
for i1, _, _ in g.triples((None, RDFS.subClassOf, ns.Person)):
  for i2, _, _ in g.triples((None, RDF.type, i1)):
    print(i2)

print("SPARQL: ")

q2 = prepareQuery(
        """
            SELECT ?individual
            WHERE{
                ?individual rdf:type/rdfs:subClassOf* ns:Person .
            }
        """,
        initNs = {"rdf": RDF, "rdfs":RDFS, "ns":ns})

for r in g.query(q2):
  print(r)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

ns = Namespace("http://somewhere#")

print("RDFLib: ")
for individual, _, _ in g.triples((None, RDF.type, ns.Person)):
    print("Individual:", individual)
    for _, prop, value in g.triples((individual, None, None)):
        print("   Property:", prop)
        print("   Value:", value)

for individual, _, _ in g.triples((None, RDF.type, ns.Animal)):
    print("Individual:", individual)
    for _, prop, value in g.triples((individual, None, None)):
        print("  Property:", prop)
        print("  Value:", value)

print("\nSPARQL: ")

from rdflib.plugins.sparql import prepareQuery

q3 = prepareQuery(
    """
    SELECT ?individual ?property ?value
    WHERE {
        {
            ?individual rdf:type ns:Person .
        }
        UNION
        {
            ?individual rdf:type ns:Animal .
        }
        ?individual ?property ?value .
    }
    """,
    initNs={"rdf": RDF, "ns": ns}
)
for r in g.query(q3):
  print(r)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

from rdflib.namespace import FOAF
from rdflib import Graph, Namespace, Literal, XSD
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns = Namespace("http://somewhere#")

print("RDFLib: ")
for r, _, _ in g.triples((None, vcard.Given, Literal('Rocky', datatype = XSD.string))):
    for person, _, _ in g.triples((None, FOAF.knows, r)):
        print(person)


print("SPARQL: ")

q4= prepareQuery("""
  SELECT ?name
  WHERE {
    {
      ?name foaf:knows ?rocky.
      ?rocky vcard:FN ?rockyFN.
      FILTER(CONTAINS(str(?rockyFN), "Rocky"))
      {
        ?name a ns:Person.
      }
      UNION
      {
        ?name a ?subClass.
        ?subClass rdfs:subClassOf ns:Person.
      }
    }
  }
  """,
  initNs = { "vcard": vcard.replace("#","/"), "rdfs":RDFS, "ns":ns, "foaf":FOAF}
)

# Visualize the results
for r in g.query(q4):
  print(r.name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

from rdflib.namespace import FOAF
from collections import defaultdict

print("RDFLib: ")

knows_count= defaultdict(set)

for s, p, o in g.triples((None, FOAF.knows, None)):
    knows_count[s].add(o)

at_least_two_entities = [entity for entity, knowns in knows_count.items() if len(knowns) >= 2]

for entity in at_least_two_entities:
    print(entity)
#SPARQL
print("SPARSQL: ")

q5= prepareQuery("""
  SELECT ?entity
  WHERE {
    ?entity foaf:knows ?person1 .
    ?entity foaf:knows ?person2 .
    FILTER (?person1 != ?person2)
  }
  GROUP BY ?entity
  HAVING (COUNT(?person1) >= 2)
  """,
  initNs = {"rdfs":RDFS, "ns":ns, "foaf":FOAF}
)

# Visualize the results
for r in g.query(q5):
  print(r.entity)
