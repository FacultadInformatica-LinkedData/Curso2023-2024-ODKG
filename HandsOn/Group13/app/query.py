
from rdflib import Graph
import datetime


def parsear_fecha(fecha_str):
    # Extrae solo la parte 'YYYY-MM-DD' de la fecha
    fecha_pura = fecha_str.split('T')[0]
    return datetime.datetime.strptime(fecha_pura, '%Y-%m-%d')

# Función para realizar consultas SPARQL y obtener datos
def obtener_datos():
    g = Graph()
    g.parse("content/data_updated.ttl", format="turtle")

    # Lista para almacenar los datos de las ubicaciones
    ubicaciones = []


    consulta = """
        SELECT ?nombreEvento ?nombreFacility ?latitud ?longitud ?fecha ?url ?horario
    WHERE {
    ?evento <http://schema.org/name> ?nombreEvento .
    ?facility <http://schema.org/name> ?nombreFacility .
    ?facility <http://schema.org/latitude> ?latitud .
    ?facility <http://schema.org/longitude> ?longitud .
    ?facility <http://madrid.encuentra.es/resource/contentURL> ?url .
    ?evento <http://schema.org/openingHoursSpecification> ?horario .
    ?evento <http://schema.org/StartDate> ?fecha .
    }
    LIMIT 20000
    """
    for row in g.query(consulta):
        nombre_evento,nombre_facility, latitud, longitud,fecha,url,horario = row
        ubicaciones.append((str(nombre_evento),str(nombre_facility), float(latitud), float(longitud),parsear_fecha(fecha),str(url),str(horario)))
    return ubicaciones