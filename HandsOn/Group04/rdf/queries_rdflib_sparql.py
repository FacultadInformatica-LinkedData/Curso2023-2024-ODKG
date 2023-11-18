from rdflib import Graph

g = Graph()
g.parse("./output-datasets.ttl", format="turtle")

##########################################
# Query: total number of cultural events #
##########################################
q1 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT (COUNT(?event) AS ?eventCount) WHERE {
      ?event a ns0:CulturalEvent .
    }
    """

print("\nSPARQL result:")
number_of_events = 0
for r in g.query(q1):
    number_of_events = int(r.eventCount)
print(f"Total number of cultural events: {number_of_events}")

# SPARQL result:
# Total number of cultural events: 1056

#############################################################
# Query: cultural events prices and frequency of each price #
#############################################################
q2 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT ?price (COUNT(?price) AS ?priceCount) WHERE {
    ?event a ns0:CulturalEvent ;
            ns0:price ?price .
    } GROUP BY ?price
    """

print("\nSPARQL result:")
prices = {}
for r in g.query(q2):
    prices[r.price] = int(r.priceCount)
for price in prices:
    price_count = prices[price]
    print(f"{price}: {price_count} events ({price_count/number_of_events*100:.2f}%)")

# SPARQL result:
# NO GRATUITO: 223 events (21.12%)
# GRATUITO: 833 events (78.88%)

#####################################################################
# Query: earliest and latest start and end dates of cultural events #
#####################################################################
q3 = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT (MIN(?startDate) AS ?earliestStartDate) (MAX(?startDate) AS ?latestStartDate)
           (MIN(?endDate) AS ?earliestEndDate) (MAX(?endDate) AS ?latestEndDate)
    WHERE {
      ?event a ns0:CulturalEvent .
      ?event ns0:startDate ?startDate .
      ?event ns0:endDate ?endDate .
    }
    """

print("\nSPARQL result:")
for r in g.query(q3):
    print(f"Earliest Start Date: {r.earliestStartDate.split('T')[0]}")
    print(f"Latest Start Date: {r.latestStartDate.split('T')[0]}")
    print(f"Earliest End Date: {r.earliestEndDate.split('T')[0]}")
    print(f"Latest End Date: {r.latestEndDate.split('T')[0]}")

# SPARQL result:
# Earliest Start Date: 2019-01-19
# Latest Start Date: 2024-01-12
# Earliest End Date: 2023-10-05
# Latest End Date: 2030-02-02

###################################################
# Query: first {limit} accessible cultural events #
###################################################
limit = 25
q4 = f"""
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT ?eventName WHERE {{
      ?event a ns0:CulturalEvent ;
             ns0:accesibility "ACCESSIBLE"^^xsd:string ;
             ns0:eventName ?eventName .
    }}
    LIMIT {limit}
    """

print("\nSPARQL result:")
print(f"First {limit} accessible events:")
for r in g.query(q4):
    print(f"{r.eventName}")

# SPARQL result:
# First 25 accessible events:
# 10 emociones, 10 rosas
# 20.000 especies de abejas
# 20.000 especies de abejas
# 23 paseos
# 24 horas
# 4 patas tiene un cuento
# 90 Salon de Otono
# A cuatro manos
# A los cuatro vientos
# A mi manera
# ABBA live in concert
# Acceso restringido
# Africa y Espana en la inspiracion teatral
# Aimistica
# Akai- Vida en cuatro haikus
# Al compas de Dobemol
# Al fuego de la literatura: autoras de novela grafica
# Alas para sonar y aletas para jugar
# Alcarras
# Alertantes del distrito
# Alfabetizacion digital
# Alicia Tamariz - Hortaleza
# Alimentacion saludable para la vida silvestre: Comederos para aves
# Alma de boqueron
# Alma de Boqueron, Rumba Mestiza de Autor.

#############################################################
# Query: name and URL of first {limit} cultural event types #
#############################################################
limit = 10
q5 = f"""
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT DISTINCT ?eventName ?eventUrl WHERE {{
      ?event a ns0:CulturalEvent ;
             ns0:hasEventType ?eventType ;
             ns0:eventName ?eventName ;
             ns0:eventUrl ?eventUrl .
    }}
    LIMIT {limit}
    """

print("\nSPARQL result")
print(f"First {limit} event types:")
for r in g.query(q5):
    print(f"{r.eventName}\n\tWebsite: {r.eventUrl}")

# SPARQL result
# First 10 event types:
# 10 emociones, 10 rosas
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=bc84a325d4ffa810VgnVCM1000001d4a900aRCRD
# 20.000 especies de abejas
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=94dd6b6c66d8a810VgnVCM2000001f4a900aRCRD
# 20.000 especies de abejas
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=4759a738045da810VgnVCM1000001d4a900aRCRD
# 23 paseos
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=e631eceda70ea810VgnVCM1000001d4a900aRCRD
# 24 horas
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=5a4ba55f80e8a810VgnVCM2000001f4a900aRCRD
# 4 patas tiene un cuento
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=c825b3a00f0ea810VgnVCM2000001f4a900aRCRD
# 4x4
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=16e9e6b609029810VgnVCM1000001d4a900aRCRD
# 6º Congreso Global de Metapoesia: la metapoesia es un genero nuevo
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=45000dae9a6da810VgnVCM2000001f4a900aRCRD
# 7º Concurso de relatos Cuarto y Mitad: 'Ojos de Besugo'
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=7d98a590d22f1810VgnVCM1000001d4a900aRCRD
# 90 Salon de Otono
#         Website: http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&vgnextoid=cbc606532e1ba810VgnVCM2000001f4a900aRCRD

###############################################################################
# Query: facility name and address of first {limit} cultural events (w/ name) #
###############################################################################
limit = 20
q6 = f"""
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT ?eventName ?facilityName ?addressName WHERE {{
    ?event a ns0:CulturalEvent ;
            ns0:eventName ?eventName ;
            ns0:hasPlace ?facility .
            
    ?facility a ns0:Facility ;
                ns0:facilityName ?facilityName ;
                ns0:hasAddress ?address .
    
    ?address a ns0:Address ;
            ns0:addressName ?addressName .
    }}
    LIMIT {limit}
    """
print("\nSPARQL result")
print(f"Facility and address of first {limit} events (w/ name):")
for r in g.query(q6):
    print(f"{r.eventName}\nFacility:\n\tName: {r.facilityName}\n\tAddress: {r.addressName}")

# SPARQL result
# Facility and address of first 20 events (w/ name):
# La Distancia entre A y B es la misma que entre B y A
# Facility:
#         Name: Museo de Arte Contemporaneo de Madrid
#         Address: CALLE CONDE DUQUE
# Animales feos y no tan feos
# Facility:
#         Name: Museo de Historia de Madrid
#         Address: CALLE FUENCARRAL
# Exposicion del IV concurso de fotografia 'Proxima estacion: Madrid'
# Facility:
#         Name: Museo de Historia de Madrid
#         Address: CALLE FUENCARRAL
# Conferencia: 'Alta, aterradora y pelirroja: la reina Boudica y la revuelta contra Roma en Britania'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'El Mediterraneo es mio': Cartago contra todos
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'El torque ensangrentado: Roma y los galos'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'Encuentros en al estepa infinita: los aquemenidas y los escitas'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'Grecia frente a los persas: las aspiraciones frustradas de Dario y Jerjes'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'Legiones contra falanges: la batalla por el Mediterraneo oriental'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'Los reinos helenisticos y sus guerras. Unos reinos desconocidos'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia: 'Roma y el imperio parto por el control de Oriente'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Conferencia:' ¡Que vienen los barbaros! Constantinopla asediada (626-1453)'
# Facility:
#         Name: Museo de San Isidro. Los Origenes de Madrid
#         Address: PLAZA SAN ANDRES
# Anton Cortes Trio. Soniquete (Latina)
# Facility:
#         Name: Auditorio y sala de exposiciones Paco de Lucia (Latina)
#         Address: AVENIDA LAS AGUILAS
# Folclore Tradicional
# Facility:
#         Name: Auditorio y sala de exposiciones Paco de Lucia (Latina)
#         Address: AVENIDA LAS AGUILAS
# Galop
# Facility:
#         Name: Auditorio y sala de exposiciones Paco de Lucia (Latina)
#         Address: AVENIDA LAS AGUILAS
# Concierto: 'POP CLaSICO'
# Facility:
#         Name: Centro Cultural Alfredo Kraus (Fuencarral - El Pardo)
#         Address: GLORIETA PRADERA DE VAQUERIZAS
# Concierto: 'THE AMBASSADORS'
# Facility:
#         Name: Centro Cultural Alfredo Kraus (Fuencarral - El Pardo)
#         Address: GLORIETA PRADERA DE VAQUERIZAS
# Cuentacuentos: 'LA TERRORiFICA HISTORIA DE ABA'
# Facility:
#         Name: Centro Cultural Alfredo Kraus (Fuencarral - El Pardo)
#         Address: GLORIETA PRADERA DE VAQUERIZAS
# Sala de Estudios
# Facility:
#         Name: Centro Cultural Alfredo Kraus (Fuencarral - El Pardo)
#         Address: GLORIETA PRADERA DE VAQUERIZAS
# Teatro: 'AQUi NO PAGA NADIE'
# Facility:
#         Name: Centro Cultural Alfredo Kraus (Fuencarral - El Pardo)
#         Address: GLORIETA PRADERA DE VAQUERIZAS
