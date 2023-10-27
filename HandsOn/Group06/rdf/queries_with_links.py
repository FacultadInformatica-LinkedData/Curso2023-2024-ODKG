from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.parse("output.ttl", format="ttl")

calle = Namespace("http://opendataandkg.org/group06/ontology/calle#")

print("__________________________________________")
print("Q1: Relation between district and wikidata")
print("__________________________________________")
q1 = prepareQuery('''
    SELECT DISTINCT ?dist ?samedist
    WHERE {
      ?calle calle:same_as_wikidata_distrito ?samedist.
      ?calle calle:distrito ?dist.
    }
    LIMIT 10

  ''',
  initNs = { "calle": calle}
)
for r in g.query(q1):
  print(r)

# Results:
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/Latina'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q794954'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/Moncloa-Aravaca'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q2017682'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/Centro'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q1763376'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/Arganzuela'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q2000929'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/Chamber%C3%AD'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q1763370'))


print("")
print("__________________________________________")
print("Q2: Relation between street and wikidata ")
print("__________________________________________")
q2 = prepareQuery('''
    SELECT DISTINCT ?calle ?samecalle 
    WHERE { 
         ?calle calle:same_as_wikidata_calle ?samecalle.
    } LIMIT 10

  ''',
  initNs = { "calle": calle}
)
for r in g.query(q2):
  print(r)


# Results:
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/calle%20de%20Fuencarral'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q5740840'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/San%20Bernardo%20street'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q5740864'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/calle%20de%20Hortaleza'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q5740911'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Carrera%20de%20San%20Jer%C3%B3nimo'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q5836422'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Calle%20de%20Atocha'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q5492657'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Calle%20Mayor'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q1149052'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Gran%20V%C3%ADa'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q1324163'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Paseo%20de%20Recoletos'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q2550870'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/calle%20de%20G%C3%A9nova'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q24294474'))
#(rdflib.term.URIRef('http://opendataandkg.org/group06/ontology/calle/resource/Calle%20de%20las%20Huertas%2C%20Madrid'), rdflib.term.Literal('https://www.wikidata.org/wiki/Q2364997'))



