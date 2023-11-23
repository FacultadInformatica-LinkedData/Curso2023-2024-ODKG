# -*- coding: utf-8 -*-
"""app.py"""

import streamlit as st
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.plugins.sparql import prepareQuery
import folium
import pandas as pd
from streamlit_folium import folium_static
import random


rdf_file_path = 'RDFapp.ttl'
graph = Graph()
graph.parse(rdf_file_path, format='turtle')


######## Filter creation ######


barrios_query = """
    SELECT DISTINCT ?neighbourhood WHERE {
        ?centro ns1:neighbourhood ?neighbourhood .
    }
    ORDER BY ?neighbourhood

"""

tipos_centros_query = """
    SELECT DISTINCT ?typeCenter WHERE {
        ?centro ns1:typeCenter ?typeCenter .
    }
    ORDER BY ?typeCenter

"""

barrios_results = graph.query(barrios_query)
tipos_centros_results = graph.query(tipos_centros_query)



barrios = [str(row['neighbourhood']) for row in barrios_results]
tipos_centros = [str(row['typeCenter']) for row in tipos_centros_results]

# Barra lateral con desplegables para filtrar 
st.sidebar.header('Filters')
selected_barrio = st.sidebar.selectbox('Select a neighbourhood:', barrios)
selected_tipo = st.sidebar.selectbox('Select a type of centre:', tipos_centros)


########## Creacion del mapa ##########

# Crear un mapa centrado en un punto específico
madrid_map_all = folium.Map(location=[40.4168, -3.7038], zoom_start=12)

# Consulta SPARQL para obtener datos de latitud y longitud
q1 = """
    SELECT ?lat ?lon ?name ?type
    WHERE {{
        ?centro rdf:type ns1:HealthCentre.
        ?centro ns2:Location ?ubicacion.
        ?ubicacion ns3:latitude ?lat.
        ?ubicacion ns3:longitude ?lon.
        ?centro ns1:name ?name.  
        ?centro ns1:typeCenter ?type.  

            
            
    }}
"""

# Ejecutar la consulta SPARQL
r1 = graph.query(q1)



# Iterar sobre los resultados de la consulta SPARQL y agregar marcadores al mapa
for row in r1:
    try:
        lat = row['lat']
        long = row['lon']
        name = row['name']
        tipo_centro = row['type']

    
       

        # Crear un marcador con un popup que contiene el nombre
        marker = folium.Marker(
            location=[lat, long],
            popup=folium.Popup(name, max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        )

        # Agregar el marcador al mapa
        marker.add_to(madrid_map_all)

    except Exception as e:
        st.warning(f"Error")





####### Boton de buscar #######



# Botón de búsqueda
if st.sidebar.button('Search'):

    
    # Limpiar la capa de marcadores existente
    madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=12)

    # Consulta SPARQL para obtener datos de latitud y longitud con filtros aplicados
    consulta_sparql = f"""
        SELECT ?lat ?lon ?name
        WHERE {{
            ?centro rdf:type ns1:HealthCentre.
            ?centro ns2:Location ?ubicacion.
            ?ubicacion ns3:latitude ?lat.
            ?ubicacion ns3:longitude ?lon.
            ?centro ns1:name ?name.
            ?centro ns2:Location ?Location.
            ?Location ns3:hasAddress ?Address.
            ?Address ns1:neighbourhood "{selected_barrio}" .
            ?centro ns1:typeCenter "{selected_tipo}" .
        }}
    """
    results = graph.query(consulta_sparql)

    # Iterar sobre los resultados de la consulta SPARQL y agregar marcadores al mapa
    for row in results:
        try:
            lat = row['lat']
            long = row['lon']
            name = row['name']

            # Crear un marcador con un popup que contiene el nombre
            marker = folium.Marker(
                location=[lat, long],
                popup=folium.Popup(name, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            )

            # Agregar el marcador al mapa
            marker.add_to(madrid_map)
        except Exception as e:
            st.warning(f"Error")

    # Mostrar el mapa actualizado en Streamlit
    folium_static(madrid_map)




    # Construir y ejecutar la consulta SPARQL con los filtros seleccionados
    consulta_sparql = f"""
        SELECT ?name ?street ?number ?districtwikidata ?phone WHERE {{
            ?centro ns2:Location ?Location.
            ?Location ns3:hasAddress ?Address.
            ?Address ns1:neighbourhood "{selected_barrio}" .
            ?centro ns1:typeCenter "{selected_tipo}" .
            ?centro ns1:name ?name .
            ?Address ns3:street-address ?street .
            ?Address ns5:hasStreetNumber ?number .
            ?Address ns1:district_wikidata ?districtwikidata .
            ?centro ns1:hasOtherInformation ?Information .
            ?Information ns7:contact ?Contact .
            ?Contact ns6:term_phone ?phone .

                        
            
        }}
    """
    results = graph.query(consulta_sparql)
    
    result_list = []
    for row in results:
        result_dict = row.asdict()
        # Combina street y number en la columna address
        result_dict['address'] = f"{result_dict['street']}, {result_dict['number']}"
        # Elimina las columnas street y number
        del result_dict['street']
        del result_dict['number']

        districtwikidata = f"{result_dict['districtwikidata']}"

        result_dict = {
            'name': result_dict['name'],
            'address': result_dict['address'],
            'phone': result_dict['phone'],
            
        }
        result_list.append(result_dict)

       
   
    
    if result_list:
        
        #result_list= result_list.fillna("No hay información")

        st.subheader(f'Results for {selected_tipo} in {selected_barrio}')
        st.table(result_list)
        st.markdown(f"For more information about the district, please consult [{districtwikidata}]({districtwikidata})")

    else:
        st.info('No results found for the selection.')
else:
    
    # Mostrar el mapa en Streamlit
    folium_static(madrid_map_all)