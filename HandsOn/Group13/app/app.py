from flask import Flask, render_template
from rdflib import Graph
from query import obtener_datos
import datetime
from folium.plugins import MarkerCluster
import folium

app = Flask(__name__)

# Ahora, 'ubicaciones' contiene todos los nombres y coordenadas
def filtrar_eventos_por_fecha(ubicaciones, fecha_inicio, fecha_fin):
    fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
    return [evento for evento in ubicaciones if fecha_inicio <= evento[4] <= fecha_fin]


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/mapa')

    # Continúa con la creación del mapa utilizando esta lista
def index():

    # Utiliza esta función para filtrar los eventos
    ubicaciones = obtener_datos()
    fecha_inicio = datetime.datetime.today()  # Fecha de inicio del filtro
    fecha_fin = '2023-12-31'    # Fecha de fin del filtro
    eventos_filtrados = filtrar_eventos_por_fecha(ubicaciones, fecha_inicio, fecha_fin)

    # Ahora crea el mapa utilizando 'eventos_filtrados'
    mapa = folium.Map(location=[40.416775, -3.703790], zoom_start=6)

    marker_cluster = MarkerCluster().add_to(mapa)

# Añade tus marcadores al cluster en lugar de directamente al mapa
    for nombreEvento, nombreFacility, latitud, longitud, Fecha, Url,horario in eventos_filtrados:
        import calendar
        my_date = Fecha
        day = calendar.day_name[my_date.weekday()]
        descripcion = f"<strong>Event:</strong> {nombreEvento}<br><strong>Facility:</strong> {nombreFacility}<br><strong>Date:</strong> {Fecha}: {day}<br><strong>Start:</strong> {horario[:5]}<br><strong>URL:</strong> <a href='{Url}' target='_blank'>{Url[:50]}...</a>"
        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(descripcion, max_width=300),
            icon=folium.Icon(icon='info-sign')
        ).add_to(marker_cluster)

    mapa.save('static/mapa2.html')
    return render_template('mapa.html')

if __name__ == '__main__':
    app.run(debug=True)