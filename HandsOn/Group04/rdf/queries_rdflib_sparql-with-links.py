from rdflib import Graph

g = Graph()
g.parse("./output-datasets-with-links.ttl", format="turtle")

##########################################
# Query: facility in Q4043800 #
##########################################
q1 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?facility WHERE {
      ?facility  owl:sameAs "https://www.wikidata.org/entity/Q4043800" .
    }
    """

print("\nSPARQL result:")
for r in g.query(q1):
    print(f"{r.facility}")

# SPARQL result:
# http://www.madculturalevents.es/group04/resources/facility/4684678

#############################################################
# Query: cultural events prices and frequency of each price #
#############################################################
q2 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT (COUNT(?event) AS ?eventCount)  WHERE {
      ?event ns0:hasAddress ?address .
      ?address ns0:belongsTo ?district .
      ?district owl:sameAs "https://www.wikidata.org/entity/Q1763376".
    }
    """

print("\nSPARQL result:")
prices = {}
for r in g.query(q2):
    print(f"Eventos en el centro de Madrid: {r.eventCount}")

# SPARQL result:
# Eventos en el centro de Madrid: 35

#####################################################################
# Query: districts with their uri's #
#####################################################################
q3 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?district ?uri  WHERE {
      ?event ns0:hasAddress ?address .
      ?address ns0:belongsTo ?district .
      ?district owl:sameAs ?uri.
} GROUP BY ?district
    """

print("\nSPARQL result:")
for r in g.query(q3):
    print(f"district: {r.district}")
    print(f"\turi: {r.uri}")

# SPARQL result:
# district: http://www.madculturalevents.es/group04/resources/district/Centro
#         uri: https://wikidata.org/entity/Q1763376
# district: http://www.madculturalevents.es/group04/resources/district/Barajas
#         uri: https://wikidata.org/entity/Q807230
# district: http://www.madculturalevents.es/group04/resources/district/Retiro
#         uri: https://wikidata.org/entity/Q2002296
# district: http://www.madculturalevents.es/group04/resources/district/Moncloa-Aravaca
#         uri: https://wikidata.org/entity/Q2017682
# district: http://www.madculturalevents.es/group04/resources/district/Ciudad%20Lineal
#         uri: https://wikidata.org/entity/Q1763694
# district: http://www.madculturalevents.es/group04/resources/district/Salamanca
#         uri: https://wikidata.org/entity/Q1773521
# district: http://www.madculturalevents.es/group04/resources/district/Chamart%C3%ADn
#         uri: https://wikidata.org/entity/Q1766348
# district: http://www.madculturalevents.es/group04/resources/district/Chamber%C3%AD
#         uri: https://wikidata.org/entity/Q1763370
# district: http://www.madculturalevents.es/group04/resources/district/Tetu%C3%A1n
#         uri: https://wikidata.org/entity/Q1773540
# district: http://www.madculturalevents.es/group04/resources/district/Latina
#         uri: https://wikidata.org/entity/Q794954
# district: http://www.madculturalevents.es/group04/resources/district/Puente%20de%20Vallecas
#         uri: https://wikidata.org/entity/Q2003054
# district: http://www.madculturalevents.es/group04/resources/district/Fuencarral-El%20Pardo
#         uri: https://wikidata.org/entity/Q656196
# district: http://www.madculturalevents.es/group04/resources/district/Arganzuela
#         uri: https://wikidata.org/entity/Q2000929       
# district: http://www.madculturalevents.es/group04/resources/district/Carabanchel
#         uri: https://wikidata.org/entity/Q1001991       
# district: http://www.madculturalevents.es/group04/resources/district/San%20Blas-Canillejas
#         uri: https://www.wikidata.org/entity/Q2001937   
# district: http://www.madculturalevents.es/group04/resources/district/Hortaleza
#         uri: https://www.wikidata.org/entity/Q1928529   
# district: http://www.madculturalevents.es/group04/resources/district/Villa%20de%20Vallecas
#         uri: https://www.wikidata.org/entity/Q1947988
# district: http://www.madculturalevents.es/group04/resources/district/Villaverde
#         uri: https://www.wikidata.org/entity/Q919536    
# district: http://www.madculturalevents.es/group04/resources/district/Usera
#         uri: https://www.wikidata.org/entity/Q953368    
# district: http://www.madculturalevents.es/group04/resources/district/Vic%C3%A1lvaro
#         uri: https://www.wikidata.org/entity/Q589403    
# district: http://www.madculturalevents.es/group04/resources/district/Moratalaz
#         uri: https://www.wikidata.org/entity/Q2076109 
