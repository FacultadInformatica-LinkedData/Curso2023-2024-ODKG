
import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to create a Folium map centered on Madrid
def create_map():
    # Coordinates of Madrid's city center
    madrid_coords = [40.4168, -3.7038]  # Latitude and longitude of Madrid
    map_madrid = folium.Map(location=madrid_coords, zoom_start=12)
    return map_madrid

# Streamlit page setup
st.title('Madrid City Map')
st.write('This map shows the city center of Madrid.')

# Display the map in the Streamlit app
madrid_map = create_map()
folium_static(madrid_map)
