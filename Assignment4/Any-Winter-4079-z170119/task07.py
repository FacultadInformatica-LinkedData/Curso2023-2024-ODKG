# -*- coding: utf-8 -*-
"""**Task 07: Querying RDF(s)**
"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g.namespace_manager.bind('ns', ns, override=False)
g.namespace_manager.bind('vcard', vcard, override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

print("TASK 7.1: List all subclasses of \"LivingThing\" with RDFLib and SPARQL")
# Here we include only subclasses of LivingThing

# RDFLib
def get_nested_subclasses(parent_class):
    sub_classes = set()
    for s, p, o in g.triples((None, RDFS.subClassOf, parent_class)):
        sub_classes.add(s)
        sub_classes.update(get_nested_subclasses(s))
    return sub_classes

# Visualize the results
print("RDFLib results:")
living_thing_sub_classes = get_nested_subclasses(ns.LivingThing)
for sub_class in living_thing_sub_classes:
    print(sub_class)

# SPARQL
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT 
    ?sub_class
  WHERE { 
    ?sub_class RDFS:subClassOf+ ns:LivingThing. 
  }
  ''',
  initNs = { "RDFS": RDFS, "ns": ns}
)

# Visualize the results
print("SPARQL results:")
for r in g.query(q1):
  print(r[0])

# RDFLib results:
# http://somewhere#Person
# http://somewhere#Researcher
# http://somewhere#PhDstudent
# http://somewhere#Professor
# http://somewhere#Animal
# SPARQL results:
# http://somewhere#Person
# http://somewhere#Researcher
# http://somewhere#PhDstudent
# http://somewhere#Professor
# http://somewhere#Animal

print("\nTASK 7.2: List all individuals of \"Person\" with RDFLib and SPARQL (remember the subClasses)")
# Here we include both Person and subclasses of Person

# RDFLib
def get_instances_and_types(class_):
    instances_and_types = set()
    for s, p, o in g.triples((None, RDF.type, class_)):
        instances_and_types.add((s, class_))
        sub_classes = get_nested_subclasses(class_)
        for sub_class in sub_classes:
            for s, p, o in g.triples((None, RDF.type, sub_class)):
                instances_and_types.add((s, sub_class))
    return instances_and_types
people_with_types = get_instances_and_types(ns.Person)

# Visualize the results
print("RDFLib results:")
for (person, type_) in people_with_types:
    print("{} (a {})".format(person, type_))

# SPARQL
q2 = prepareQuery('''
  SELECT 
    ?individual ?type
  WHERE { 
    ?individual RDF:type ?type.
    ?type RDFS:subClassOf* ns:Person.
  }
  ''',
  initNs = { "RDFS": RDFS, "RDF": RDF, "ns": ns}
)

# Visualize the results
print("SPARQL results:")
for r in g.query(q2):
    print("{} (a {})".format(r[0], r[1]))

# RDFLib results:
# http://somewhere#JohnSmith (a http://somewhere#Person)
# http://somewhere#SaraJones (a http://somewhere#Person)
# http://somewhere#JimGonzalez (a http://somewhere#Professor)
# http://somewhere#JaneSmith (a http://somewhere#Researcher)
# SPARQL results:
# http://somewhere#SaraJones (a http://somewhere#Person)
# http://somewhere#JohnSmith (a http://somewhere#Person)
# http://somewhere#JaneSmith (a http://somewhere#Researcher)
# http://somewhere#JimGonzalez (a http://somewhere#Professor)

print("\nTASK 7.3: List all individuals of \"Person\" or \"Animal\" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person")

# RDFLib (Visualizing the results)
animals_with_types = get_instances_and_types(ns.Animal)
people_and_animals_with_types = set()
people_and_animals_with_types.update(people_with_types, animals_with_types)
print("RDFLib results:")
for (person_or_animal, type_) in people_and_animals_with_types:
    print("{} (a {})".format(person_or_animal, type_))
    for s, p, o in g.triples((person_or_animal, None, None)):
        print("\t\t{}".format(p))

# SPARQL
q3 = prepareQuery('''
  SELECT 
    ?individual ?type ?property
  WHERE { 
    ?individual RDF:type ?type.
    ?individual ?property ?value.
    {?type RDFS:subClassOf* ns:Person} UNION {?type RDFS:subClassOf* ns:Animal}
  }
  ''',
  initNs = { "RDFS": RDFS, "RDF": RDF, "ns": ns}
)

# Visualize the results
print("SPARQL results:")
individuals = {}
for r in g.query(q3):
    individual, type_, property_, = r
    if not individual in individuals.keys():
        individuals[individual] = {
            "type": type_,
            "property": [property_]
        }
    else:
        individuals[individual]["property"].append(property_)
for key, values in individuals.items():
    print("{} (a {})".format(key, values["type"]))
    for property_ in values["property"]:
        print("\t\t{}".format(property_))

# RDFLib results:
# http://somewhere#JimGonzalez (a http://somewhere#Professor)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
# http://somewhere#SaraJones (a http://somewhere#Person)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# http://somewhere#RockySmith (a http://somewhere#Animal)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# http://somewhere#JohnSmith (a http://somewhere#Person)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
# http://somewhere#JaneSmith (a http://somewhere#Researcher)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# SPARQL results:
# http://somewhere#RockySmith (a http://somewhere#Animal)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# http://somewhere#SaraJones (a http://somewhere#Person)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# http://somewhere#JohnSmith (a http://somewhere#Person)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
# http://somewhere#JaneSmith (a http://somewhere#Researcher)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family
#                 http://xmlns.com/foaf/0.1/knows
#                 http://xmlns.com/foaf/0.1/knows
# http://somewhere#JimGonzalez (a http://somewhere#Professor)
#                 http://www.w3.org/1999/02/22-rdf-syntax-ns#type
#                 http://www.w3.org/2001/vcard-rdf/3.0/Given
#                 http://www.w3.org/2001/vcard-rdf/3.0/FN
#                 http://www.w3.org/2001/vcard-rdf/3.0/Family

print("\nTASK 7.4:  List the name of the persons who know Rocky")

# SPARQL
from rdflib import FOAF
q4 = prepareQuery('''
  SELECT 
    ?full_name
  WHERE { 
    ?individual RDF:type ?type.
    ?type RDFS:subClassOf* ns:Person.
    ?individual FOAF:knows ns:RockySmith.
    ?individual vcard:FN ?full_name
  }
  ''',
  initNs = { "FOAF": FOAF, "RDFS": RDFS, "RDF": RDF, "ns": ns, "vcard": vcard}
)

# Visualize the results
print("SPARQL results:")
for r in g.query(q4):
    print(r[0])

# SPARQL results:
# Sara Jones
# Jane Smith

print("\nTask 7.5: List the entities who know at least two other entities in the graph")
# RDFLib (Visualizing the results)
acquaintances = {}
for s, p, o in g.triples((None, FOAF.knows, None)):
    if not s in acquaintances.keys():
        acquaintances[s] = [o]
    else:
        acquaintances[s].append(o)

for self_, own_acquaintances in acquaintances.items():
    if len(own_acquaintances) > 1:
        print("{} knows".format(self_))
        for acquaintance in own_acquaintances:
            print("\t\t{}".format(acquaintance))
# RDFLib results:
# http://somewhere#RockySmith knows
#                 http://somewhere#JaneSmith
#                 http://somewhere#SaraJones
# http://somewhere#SaraJones knows
#                 http://somewhere#JaneSmith
#                 http://somewhere#RockySmith
# http://somewhere#JaneSmith knows
#                 http://somewhere#SaraJones
#                 http://somewhere#RockySmith
