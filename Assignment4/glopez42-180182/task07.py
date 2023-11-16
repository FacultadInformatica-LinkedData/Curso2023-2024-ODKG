"""Task07.ipynb

**Task 07: Querying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib.plugins.sparql import prepareQuery

g = Graph()
ns = Namespace("http://somewhere#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.namespace_manager.bind('ns', ns, override=False)
g.namespace_manager.bind('vcard', VCARD, override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

print("**TASK 7.1**")

print("Using rdflib:")

def print_subclasses(class_uri, level):
    if level == 0: # prints the "father" class at the begining
        print(class_uri)
    level = level + 1
    for s, p, o in g.triples((None, RDFS.subClassOf, class_uri)):
        print(s)
        print_subclasses(s, level)

print_subclasses(ns.LivingThing, 0)

print("Using SPARQL:")
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf* ns:LivingThing. 
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)

for r in g.query(q1):
  print(r.Subject)

print()


"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""
print("**TASK 7.2**")

print("Using rdflib:")

def get_subclasses(class_uri):
    subclasses = [class_uri]
    for s,p,o in g.triples((None, RDFS.subClassOf, class_uri)):
        subclasses = subclasses + get_subclasses(s)
    return subclasses

subclasses = get_subclasses(ns.Person)

for object in subclasses:
    for s,p,o in g.triples((None, RDF.type, object)):
      print(s)

print("Using SPARQL:")
q1 = prepareQuery('''
  SELECT DISTINCT ?Subject WHERE { 
    {
        ?Subject rdf:type ns:Person. 
    }
    UNION {
        ?class rdfs:subClassOf* ns:Person.
        ?Subject rdf:type ?class.
    }
  }
  ''',
  initNs = { "rdf":RDF ,"rdfs": RDFS, "ns": ns}
)

for r in g.query(q1):
  print(r.Subject)

print()

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""
print("**TASK 7.3**")

print("Using rdflib:")
subclasses = [ns.Person, ns.Animal]

for object in subclasses:
    for s,p,o in g.triples((None, RDF.type, object)):
      print("Individual: ", end="")
      print(s)
      print("Class type: ", end="")
      print(object)
      for s1,p1,o1 in g.triples((s, None, None)):
         print("- Property: ", end="")
         print(p1)

print()
print("Using SPARQL:")
q1 = prepareQuery('''
  SELECT ?Individual ?Property ?Value WHERE { 
    {
      ?Individual rdf:type ns:Person.
    }
    UNION
    {
      ?Individual rdf:type ns:Animal.
    }
    ?Individual ?Property ?Value.
  }
  ''',
  initNs = { "rdf": RDF, "ns": ns}
)

for r in g.query(q1):
  print(f"Individual: {r.Individual} - Property: {r.Property} - Value: {r.Value}")

print()

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

print("**TASK 7.4**")
print("Using rdflib:")

subclasses = [s for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person))]
subclasses.append(ns.Person)

for object in subclasses:
    for s,p,o in g.triples((None, RDF.type, object)):
       for s1,p1,o1 in g.triples((s, FOAF.knows, ns.RockySmith)):
          print(f"Individual: {s}")

print()

print("Using SPARQL:")

q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    {
        ?Subject rdf:type ns:Person. 
    }
    UNION {
    ?class rdfs:subClassOf ns:Person.
    ?Subject rdf:type ?class.
    }
    ?Subject foaf:knows ns:RockySmith.
  }
  ''',
  initNs = { "rdf":RDF ,"rdfs": RDFS, "ns": ns, "foaf": FOAF}
)

for r in g.query(q1):
  print(f"Individual: {r.Subject}")

print()

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

print("**TASK 7.5**")
print("Using rdflib:")

entities = [s for s,p,o in g.triples((None, FOAF.knows, None))]
checked = []
for entity in entities:
   if entities.count(entity) >= 2 and entity not in checked:
        print(f"Individual: {entity}")
        checked.append(entity)

print("Using SPARQL:")

q1 = prepareQuery('''
  SELECT DISTINCT ?Subject WHERE { 
    {
        ?Subject foaf:knows ?o1.
        ?Subject foaf:knows ?o2.
        FILTER (?o1 != ?o2)
    }
  }
  ''',
  initNs = { "foaf":FOAF }
)

for r in g.query(q1):
  print(f"Individual: {r.Subject}")
