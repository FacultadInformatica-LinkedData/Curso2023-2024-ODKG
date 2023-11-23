from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery
from rdflib_endpoint import SparqlRouter
from typing import Tuple, Optional, Any, List, Dict
from rdflib.namespace import RDF, RDFS, Namespace, GEO
import pandas as pd
import math
from fastapi.middleware.cors import CORSMiddleware



BASE_PATH = Path(__file__).resolve().parent
print(BASE_PATH)
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "colorlib-search-3"))

app = FastAPI(title="Charging Station API", openapi_url="/openapi.json")

api_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to be more restrictive as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    query = prepareQuery("""
            PREFIX ont: <https://www.chargeup.io/group07/ontology#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?station ?label ?address WHERE {
                ?station a ont:ChargingStation .
                ?station ont:hasStreetAddress ?address .
                ?station rdfs:label ?label .
            }
            """)
    results = g.query(query)
    station = [
        {"stations": str(result[0]),
         "label": str(result[1]),
         "address": str(result[2]),
         }
        for result in results]
    return TEMPLATES.TemplateResponse(
        "index1.html",
        {"request": request, "stations": station}
    )


@api_router.get("/search/", status_code=200)
def search_station(
        keyword: Optional[str] = Query(None, min_length=3, examples="BMW"),
        max_results: Optional[int] = 10
) -> dict:
    """
    To implement: Search for stations based on label keyword
    """
    pass


@api_router.get("/cities/", status_code=200)
def get_cities() -> any:
    """Get all the cities existing in the knowledge graph."""
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    query = prepareQuery("""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?city ?label ?dbpedia_city WHERE {
        ?city a ont:City .
        ?city rdfs:label ?label .
        ?city <http://www.w3.org/2002/07/owl#sameAs> ?dbpedia_city
    }
    """)
    results = g.query(query)
    output = [{"city": str(result[0]),
               "label": str(result[1]),
               "dbpedia_city": str(result[2])
               } for result in results]
    return output


@api_router.get("/stations/", status_code=200)
def get_stations() -> any:
    """Get all the stations and their street adresses"""
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    query = prepareQuery("""
        PREFIX ont: <https://www.chargeup.io/group07/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?station ?label ?address WHERE {
            ?station a ont:ChargingStation .
            ?station ont:hasStreetAddress ?address .
            ?station rdfs:label ?label .
        }
        """)
    results = g.query(query)
    output = [
              {"station": str(result[0]),
               "label": str(result[1]),
               "address": str(result[2]),
               }
              for result in results]
    return output


@api_router.get("/station-by-city/", status_code=200)
def get_station_by_city(
        city: Optional[str] = Query(None, min_length=3, examples="Darien"),
        max_results: Optional[int] = 10
) -> dict:
    """To implement: lower case indifference"""
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    SELECT ?station ?address ?city
    WHERE {{
        ?station a ont:ChargingStation .
        ?station ont:hasStreetAddress ?address .
        ?address ont:hasCity ?city .
        ?city rdfs:label "{city}" .
    }}
    LIMIT {max_results}
    """)
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "address": str(result[1]),
         "city": str(result[2]),
         }
        for result in results]
    return output

#new
#searching the charging station by the name of the city
@api_router.get("/station-by-city2/", status_code=200)
def get_station_by_city(
        city: Optional[str] = Query(None, min_length=3, examples="Darien"),
        max_results: Optional[int] = 10
) -> dict:
    """Retrieve charging stations given the city name with case insensitivity."""
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?station ?address ?cityURI
    WHERE {{
        ?station a ont:ChargingStation .
        ?station ont:hasStreetAddress ?address .
        ?address ont:hasCity ?cityURI .
        ?cityURI rdfs:label ?cityLabel .
        FILTER(LCASE(str(?cityLabel)) = LCASE("{city}")) .
    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "address": str(result[1]),
         "city": str(result.cityURI),
        }
        for result in results]
    
    return output

#new 
#searching the city by the name of the charging station
@api_router.get("/city-by-station/", status_code=200)
def get_station_by_city(
        station: Optional[str] = Query(None, min_length=3, examples="Bmw-Of-Darien"),
        max_results: Optional[int] = 10
) -> dict:
    
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    # Adjusted SPARQL query to select the city URI and to be case-insensitive
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?cityURI ?address ?station
    WHERE {{
        FILTER(LCASE(str(?stationlabel)) = LCASE("{station}")) .
        ?station rdfs:label ?stationlabel .
        ?station a ont:ChargingStation .
        ?station ont:hasStreetAddress ?address .
        ?address ont:hasCity ?cityURI .

    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "address": str(result[1]),
        }
        for result in results]
    
    return output

#new 
#searching access day time through the name of the charging station
@api_router.get("/Access-Day-Time/", status_code=200)
def get_station_by_city(
        station: Optional[str] = Query(None, min_length=3, examples="Bmw-Of-Darien"),
        max_results: Optional[int] = 10
) -> dict:
    
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    # Adjusted SPARQL query to select the city URI and to be case-insensitive
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?station ?dayTime
    WHERE {{
        FILTER(LCASE(str(?stationlabel)) = LCASE("{station}")) .
        ?station rdfs:label ?stationlabel .
        ?station a ont:ChargingStation .
        ?station ont:accessDaysTime ?dayTime .

    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "dayTime": str(result[1]),
        }
        for result in results]
    
    return output

#new 
#searching Additional Info through the name of the charging station
@api_router.get("/Additional-Info/", status_code=200)
def get_station_by_city(
        station: Optional[str] = Query(None, min_length=3, examples="Bmw-Of-Darien"),
        max_results: Optional[int] = 10
) -> dict:
    
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    # Adjusted SPARQL query to select the city URI and to be case-insensitive
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?station ?additionalInfo
    WHERE {{
        FILTER(LCASE(str(?stationlabel)) = LCASE("{station}")) .
        ?station rdfs:label ?stationlabel .
        ?station a ont:ChargingStation .
        ?station ont:additionalInfo ?additionalInfo .

    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "additionalInfo": str(result[1]),
        }
        for result in results]
    
    return output

#new 
#searching the number of specific charging station types
@api_router.get("/Number-of-Charging-Type/", status_code=200)
def get_station_by_city(
        station: Optional[str] = Query(None, min_length=3, examples="Bmw-Of-Darien"),
        max_results: Optional[int] = 10
) -> dict:
    
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?station ?evDC ?ev1 ?ev2
    WHERE {{
        FILTER(LCASE(str(?stationlabel)) = LCASE("{station}")) .
        ?station rdfs:label ?stationlabel .
        ?station a ont:ChargingStation .
        ?station ont:evDCFastCount ?evDC .
        ?station ont:evLevel1EVSENum ?ev1 .
        ?station ont:evLevel2EVSENum ?ev2 .

    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "evDC": str(result[1]),
         "ev1": str(result[2]),
         "ev2": str(result[3]),
        }
        for result in results]
    
    return output


#new 
#searching the longitude and the latitude by the name of the station
@api_router.get("/Lat-Long/", status_code=200)
def get_station_by_city(
        station: Optional[str] = Query(None, min_length=3, examples="Bmw-Of-Darien"),
        max_results: Optional[int] = 10
) -> dict:
    
    g = Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle")
    
    query = prepareQuery(f"""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT ?station ?lat ?long 
    WHERE {{
        FILTER(LCASE(str(?stationlabel)) = LCASE("{station}")) .
        ?station rdfs:label ?stationlabel .
        ?station a ont:ChargingStation .
        ?station geo:latitude ?lat .
        ?station geo:longitude ?long .

    }}
    LIMIT {max_results}
    """, initNs={"rdfs": RDFS, "ont": Namespace("https://www.chargeup.io/group07/ontology#")})
    
    results = g.query(query)
    output = [
        {"station": str(result[0]),
         "latitude": str(result[1]),
         "longitude": str(result[2]),
        }
        for result in results]
    
    return output

##################################################################

sparql_router = SparqlRouter(
    graph=Graph().parse(str(BASE_PATH / "data" / "rdf-withlinks.ttl"), format="turtle"),
    path="/chargy/",
    title="SPARQL endpoint for RDFLib graph",
    description='Our charger sparql endpoint',
    version="0.1.0",
    public_url='https://my-endpoint-url/',
    example_query="""
    PREFIX ont: <https://www.chargeup.io/group07/ontology#>
    SELECT ?city WHERE {
        ?city a ont:City .
    }
    LIMIT 5
    """
)
app.include_router(api_router)  # Basic router coming from FastAPI
app.include_router(sparql_router)  # Router taken from rdflib


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")