from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery

# Load data
g = Graph()
g.parse("../con_distritos.ttl", format="ttl")

# Queries
calle = Namespace("http://opendataandkg.org/group06/ontology/calle#")
peaton = Namespace ("http://opendataandkg.org/group06/ontology/peatones#")

##########################################################################
# Query 1

print("Q1: Get all the zip codes")
q1 = prepareQuery('''
    SELECT DISTINCT ?codigoPostal
    WHERE {
      ?calle a calle:Calle .
      ?calle calle:codigoPostal ?codigoPostal .
    }

  ''',
  initNs = { "calle": calle}
)
for r in g.query(q1):
  print(r)


#############################################################################
# Query 2

print("Q2: Get all the districts")
q2 = prepareQuery('''
    SELECT DISTINCT ?distrito
    WHERE {
      ?calle a calle:Calle .
      ?calle calle:distrito ?distrito .
    }

  ''',
  initNs = { "calle": calle}
)
for r in g.query(q2):
  print(r)


###########################################################################
# Query 3

print("Q3: Get all the distinct streets with numPeatones > 800")
q3 = prepareQuery('''
    SELECT DISTINCT ?perteneceACalle 
        WHERE {
          ?peaton a peaton:Peaton .
          ?peaton peaton:numPeatones ?numPeatones .
          FILTER (xsd:float(?numPeatones) > 800.0)
          ?peaton peaton:fechaHora ?fechaHora .
          ?peaton peaton:perteneceACalle ?perteneceACalle .
        }
  ''',
  initNs = { "peaton": peaton}
)
for r in g.query(q3):
  print(r)

###########################################################################
# Query 4

print("Q4: Get the sum of numPeatones in Calle Toledo in 2021")
q4 = prepareQuery('''
    SELECT (SUM(?numPeatones) as ?totalNumPeatones)
        WHERE {
          ?peaton a peaton:Peaton ;
                  peaton:fechaHora ?fechaHora ;
                  peaton:numPeatones ?numPeatones ;
                  peaton:perteneceACalle <http://opendataandkg.org/group06/ontology/calle/resource/Calle%20Toledo> .

          FILTER (STRSTARTS(STR(?fechaHora), "2021"))
        }
  ''',
  initNs = { "peaton": peaton, "calle":calle}
)
for r in g.query(q4):
  print(r)