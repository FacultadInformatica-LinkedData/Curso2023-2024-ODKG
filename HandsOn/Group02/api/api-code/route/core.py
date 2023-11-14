import requests
import pyproj
import warnings

# Desactivar advertencias FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Helios URL endpoint to make queries from the RDF
URL_HELIOS = "http://localhost:9000/api/sparql"


def completar_distrito(filtro, result):
    if filtro == 'default':
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
            PREFIX gn: <http://www.geonames.org/ontology#>

            SELECT DISTINCT ?nombre
                    WHERE {{
                        ?dist rdf:type esadm:Distrito.
                        ?dist gn:name ?nombre.
                    }} ORDER BY ?nombre
            """
    else:
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
        PREFIX gn: <http://www.geonames.org/ontology#>
    
        SELECT DISTINCT ?nombre
                WHERE {{
                    ?dist rdf:type esadm:Distrito.
                    ?dist gn:name ?nombre.
                    FILTER(STRSTARTS(LCASE(?nombre), "{}")).
                }} ORDER BY ?nombre
        """.format(filtro)

    params = {
        "query": query
    }

    response = requests.get(URL_HELIOS, params=params)

    if response.status_code == 200:
        data = response.json()
        result['nombres'] = [item['nombre']['value'] for item in data['results']['bindings']]
        print("Petición helios éxito")
        return result
    else:
        # Si la solicitud no se completó con éxito, muestra el código de estado
        print(f"Error: Código de estado {response.status_code}")
        return result


def buscar_locales(filtro, result):
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX madridonc: <http://madridalfresco.es/lcc/ontology/locales#>
    PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX escom: <http://vocab.linkeddata.es/datosabiertos/def/comercio/tejido-comercial#>
    PREFIX coord: <http://purl.org/net/cartCoord#>
    PREFIX gtfs: <http://vocab.gtfs.org/gtfs.ttl#>
    
    SELECT DISTINCT ?local ?coordX ?coordY ?horaCierre ?horaApertura ?rotulo ?situacion ?mesas ?sillas ?superficie ?sameAsNombreDistrito
        WHERE {{
            ?dist rdf:type esadm:Distrito.
            ?dist gn:name ?nombreDelDistrito;
                   madridonc:sameAsNombreDistrito ?sameAsNombreDistrito.
            ?local rdf:type escom:LocalComercial.
            ?local esadm:distrito ?dist;
                   coord:xcoord ?coordX;
                   coord:ycoord ?coordY;
                   gtfs:endTime ?horaCierre;
                   gtfs:startTime ?horaApertura;
                   escom:tieneTerraza ?terraza;
                   escom:rotulo ?rotulo;
                   escom:tipoSituacion ?situacion.
            ?terraza escom:numeroMesasAutorizadas ?mesas;
                    escom:numeroSillasAutorizadas ?sillas;
                    escom:superficie ?superficie.
            FILTER(LCASE(?nombreDelDistrito) = "{}").
        }}""".format(str(filtro).lower())

    params = {
        "query": query
    }

    response = requests.get(URL_HELIOS, params=params)

    if response.status_code == 200:
        # Muestra la respuesta JSON (si la API devuelve datos en formato JSON)
        data = response.json()

        for item in data['results']['bindings']:
            latitud, longitud = utm_to_latlon(item['coordX']['value'], item['coordY']['value'])
            local = {
                "local": item['local']['value'],
                "sameAsNombreDistrito": item['sameAsNombreDistrito']['value'],
                "lat": str(latitud),
                "long": str(longitud),
                "horaCierre": item['horaCierre']['value'],
                "horaApertura": item['horaApertura']['value'],
                "rotulo": item['rotulo']['value'],
                "situacion": item['situacion']['value'],
                "mesas": item['mesas']['value'],
                "sillas": item['sillas']['value'],
                "superficie": item['superficie']['value']
            }
            result['locales'].append(local)
        print("Petición helios éxito")
        return result

    else:
        # Si la solicitud no se completó con éxito, muestra el código de estado
        print(f"Error: Código de estado {response.status_code}")
        return result


def utm_to_latlon(coord_x, coord_y, zona_utm=30, hemisferio='N'):
    # Define el sistema de coordenadas UTM y el sistema de coordenadas de latitud y longitud (WGS84)
    utm = pyproj.Proj(proj='utm', zone=zona_utm, ellps='WGS84', south=(hemisferio == 'S'))
    latlon = pyproj.Proj(proj='latlong', datum='WGS84')

    # Realiza la conversión
    longitud, latitud = pyproj.transform(utm, latlon, coord_x, coord_y)

    return latitud, longitud
