from flask import Flask, render_template, request
from math import radians, sin, cos, sqrt, atan2
import requests
import urllib

# Creación de la aplicación
app = Flask(__name__)


prefixes = """PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
                PREFIX vcard: <http://www.owl-ontologies.com/vcard#> 
                PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
                PREFIX gn: <http://www.geonames.org/ontology#> 
                PREFIX ns: <http://www.RostockEVCharging.de/ontology/> 
                PREFIX nscs: <http://www.RostockEVCharging.de/ontology/resource/charging_station#> 
                PREFIX nsm: <http://www.RostockEVCharging.de/ontology/resource/municipality#> 
                PREFIX nso: <http://www.RostockEVCharging.de/ontology/resource/operator#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            """

def get_all_stations(operating_mode=None, all_day_open=False):
    
    query_open = "" if all_day_open is None else '?cs ns:opening_hours "24/7"^^xsd:string .'
    query_operating_mode = "" if operating_mode == 'none' else f'?cs ns:operating_mode "{operating_mode}"^^xsd:string .'

    query = prefixes + """SELECT DISTINCT ?cs ?cs_name ?lat ?long WHERE {
                    ?cs a ns:ChargingStation .
                    ?cs rdfs:label ?cs_name .
                    ?cs geo:lat ?lat .
                    ?cs geo:long ?long .
                    """ + query_open + """
                    """ + query_operating_mode + """
                }
                ORDER BY ?cs_name
                """
    print(query)
    response = requests.get(f"http://localhost:9000/api/sparql?query={urllib.parse.quote_plus(query)}")

    stations = []
    if 'results' in response.json():
        for station in response.json()["results"]["bindings"]:
            station_id = station["cs"]["value"].split("#")[-1]
            stations.append({"id": station_id,
                                "name": station["cs_name"]["value"],
                                "latitude": float(station["lat"]["value"]),
                                "longitude": float(station["long"]["value"])})

    else:
        stations.append(["No results found"])

    return stations

def get_station_by_id(station_id):
    query = prefixes + f"""select distinct ?cs_name ?str ?hn ?hnadd ?pc ?cards ?chp ?chp_ty ?sch ?op_m ?cost ?url ?mun ?mun_wd ?op ?op_wd WHERE {{
                    nscs:{station_id} a ns:ChargingStation .
                    nscs:{station_id} rdfs:label ?cs_name .

                    nscs:{station_id} ns:street_name ?str .
                    nscs:{station_id} ns:house_number ?hn .
                    optional {{nscs:{station_id} ns:house_number_add ?hnadd .}}
                    nscs:{station_id} ns:postal_code ?pc .

                    optional {{nscs:{station_id} ns:accepted_cards ?cards.}}
                    nscs:{station_id} ns:num_charging_points ?chp .
                    nscs:{station_id} ns:types_charging_points ?chp_ty .
                    optional {{nscs:{station_id} ns:opening_hours ?sch .}}
                    optional {{nscs:{station_id} ns:operating_mode ?op_m .}}
                    optional {{nscs:{station_id} ns:cost ?cost .}}
                    optional {{nscs:{station_id} vcard:hasURL ?url .}}

                    nscs:{station_id} gn:locatedIn ?municipality .
                    ?municipality a ns:Municipality .
                    ?municipality gn:name ?mun .
                    optional {{?municipality owl:sameAs ?mun_wd .}}

                    nscs:{station_id} ns:managed_by ?operator .
                    ?operator a ns:Operator .
                    ?operator rdfs:label ?op .
                    optional {{?operator owl:sameAs ?op_wd .}}
                    }}
                """

    response = requests.get(f"http://localhost:9000/api/sparql?query={urllib.parse.quote_plus(query)}")

    station_json = {}
    if 'results' in response.json():
        for station in response.json()["results"]["bindings"]:
            station_json['name'] = station["cs_name"]["value"]
            station_json['street'] = station["str"]["value"]
            station_json['house_number'] = station["hn"]["value"]
            if "hnadd" in station:
                station_json['house_number_add'] = station["hnadd"]["value"]
            station_json['postal_code'] = station["pc"]["value"]

            if "cards" in station:
                station_json['accepted_cards'] = station["cards"]["value"].split(";")
            station_json['num_charging_points'] = station["chp"]["value"]
            station_json['types_charging_points'] = station["chp_ty"]["value"].split(";")
            if "sch" in station:
                station_json['opening_hours'] = station["sch"]["value"]
            if "op_m" in station:
                station_json['operating_mode'] = station["op_m"]["value"]
            if "cost" in station:
                station_json['cost'] = station["cost"]["value"]
            if "url" in station:
                station_json['url'] = station["url"]["value"]
                
            station_json['municipality'] = station["mun"]["value"]
            if "mun_wd" in station:
                station_json['municipality_wd'] = station["mun_wd"]["value"]

            station_json['operator'] = station["op"]["value"]
            if "op_wd" in station:
                station_json['operator_wd'] = station["op_wd"]["value"]

    else:
        station_json.append(["No results found"])

    return station_json

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers (you can adjust this based on your needs)
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/get_stations', methods=['POST'])
def get_stations():
    # Get the latitude and longitude values from the form
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return """
        <script>
            alert('Invalid input. Please enter valid float for latitude and longitude.');
            window.history.back();
        </script>
        """

    # Calculate the distance between the user and all the charging stations
    operating_mode = request.form.get('operating_mode')
    all_day_open = request.form.get('all_day_open')
    all_stations = get_all_stations(operating_mode=operating_mode, all_day_open=all_day_open)

    for station in all_stations:
        station["distance"] = haversine_distance(latitude, longitude, station["latitude"], station["longitude"])

    # Sort the charging stations by distance
    all_stations.sort(key=lambda s: s["distance"])
    all_stations = all_stations[:5]

    return render_template("results.html", latitude=latitude, longitude=longitude, all_stations=all_stations)

@app.route('/get_station')
def get_station():
    station_id = request.args.get('id')
    station = get_station_by_id(station_id)
    return render_template("station.html", station=station)


# Init the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

