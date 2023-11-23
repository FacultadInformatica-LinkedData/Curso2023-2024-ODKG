import streamlit as st
import requests
import pandas as pd


ENDPOINT = "http://localhost:3030/University/sparql"

BASE = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <https://dbpedia.org/ontology/>
PREFIX ns: <http://www.semanticweb.org/upm/opendata/group08/ontology/UniversityInformation#>
PREFIX schema: <https://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>


SELECT DISTINCT ?nameUni ?nameCity ?longitude ?latitude ?gRate ?website ?uriUniWikiData WHERE {
    ?university rdf:type ns:University.
    ?university dbo:city ?city .
    ?city rdf:label ?nameCity.
    ?university owl:sameAs ?uriUniWikiData.
    ?university rdf:label ?nameUni. 
    ?university ns:hasRanking ?ranking .
    ?ranking ns:score ?score.
    ?university schema:longitude ?longitude.
    ?university schema:latitude ?latitude.
    ?university ns:website ?website.
    ?university ns:hasRate ?rate .
    ?rate rdf:type ns:AverageGraduationRate.
    ?rate ns:value ?gRate.
    ?university dbo:state ?state.
    ?state rdf:label ?stateName.
"""


@st.cache_data
def request(state:str= None) -> pd.DataFrame:

    df = None

    payload = BASE 

    if state:
        payload+= 'FILTER (xsd:string(?stateName) = "'+ state + '"^^xsd:string)'
    
    payload+= "} LIMIT 100"

    headers = {
        'Content-Type': 'application/sparql-query',
        'Accept': 'application/json'
    }

    try:
        response = requests.request(
            "POST", ENDPOINT, headers=headers, data=payload)



        if response.status_code == 200:
            data = response.json()

            bindings = data["results"]["bindings"]

            data_list = [
                {
                    "nameUni": item["nameUni"]["value"],
                    "nameCity": item["nameCity"]["value"],
                    "website": "www." + item["website"]["value"],
                    "uriUniWikiData": item["uriUniWikiData"]["value"],
                    "latitude": float(item["latitude"]["value"]),
                    "longitude": float(item["longitude"]["value"]),
                    "gRate": int(item["gRate"]["value"])
                }
                for item in bindings
            ]

            df = pd.DataFrame(data_list)

        else:
            print(response.text)

    except:
        print("Error")

    return df

if __name__ == "__main__":

    print(request())
