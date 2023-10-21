import morph_kgc
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS, FOAF
from rdflib.plugins.sparql import prepareQuery

config = """
    [CONFIGURATION]
    output_file= HandsOn/Group08/rdf/US-News-Rankings-Universities-Through-2023.ttl
    [DataSource1]
    mappings= HandsOn/Group08/mappings/US-News-Rankings-Liberal-Arts-Colleges-Through-2023/US-News-Rankings-Liberal-Arts-Colleges-Through-2023.ttl
         """

g = morph_kgc.materialize(config)

print(g)
