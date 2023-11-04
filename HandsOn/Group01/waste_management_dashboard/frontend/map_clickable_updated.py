import streamlit as st
import folium
from streamlit_folium import folium_static
from folium import GeoJson
import geojson
import random


# 21 districts names list
district_names = ['Arganzuela', 'Barajas', 'Carabanchel', 'Centro', 'Chamartin', 'Chamberi', 
                  'Ciudad Lineal', 'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca',
                  'Moratalaz', 'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blas', 'Tetuan',
                  'Usera', 'Vicalvaro', 'Villa de Vallecas', 'Villaverde']  

# read all .geojson file 
geojson_data = {}
for district_name in district_names:
    file_path = f'./Districts/{district_name}.geojson'
    with open(file_path, 'r') as f:
        geojson_data[district_name] = geojson.load(f)


# Create a map
m = folium.Map(location=[40.416775, -3.703790], zoom_start=12)


# Generates random colors in the format #RRGGBB
def random_color():
    return f'#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}'

# layers of each district
for dstrict in district_names:
    geojson_layer_Centro = GeoJson(
        geojson_data[dstrict],
        name = dstrict,
        style_function=lambda x: {'fillColor': random_color(), 'color': random_color()},  
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},  
        )
    # Adding a tooltip for hover
    geojson_layer_Centro.add_child(folium.features.GeoJsonTooltip(fields=['name']))
    geojson_layer_Centro.add_child(folium.ClickForMarker(popup='You clicked here!'))  # Adding a popup, replace to URL to redirect, maybe there is better way to do the redirection
    geojson_layer_Centro.add_to(m)

# Add a click listener
def on_click(feature, **kwargs):
    st.session_state.clicked_feature = feature['properties']['name']

# Add a placeholder to display info about the clicked feature
clicked_info = st.empty()

# Display the map
folium_static(m)

