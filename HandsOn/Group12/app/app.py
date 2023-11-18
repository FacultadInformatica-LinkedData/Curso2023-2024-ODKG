import dash
import plotly.express as px
import re
import pandas as pd
from dash import dcc, html, Input, Output, callback
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Namespace, Literal

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions=True

# Cargar el contenido en un grafo RDF
g = Graph()
g.parse('parkingslot_RDF_with_links-updated.ttl', format='turtle')

#ontology names
NS1=Namespace("http://grupo12_open_data.es/lcc/resource#")
NS2=Namespace("http://grupo12_open_data.org#")
NS3=Namespace("http://schema.org#")
NS4=Namespace("http://schema.mobivoc.org/")
NS5=Namespace("https://dbpedia.org/ontology/")
OWL=Namespace("http://www.w3.org/2002/07/owl#")
XSD=Namespace("http://www.w3.org/2001/XMLSchema#")


#lista de los dropdown - DISTRITOS 

q1 = prepareQuery("""
         PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
         PREFIX ns2: <http://grupo12_open_data.org#>
         PREFIX ns3: <http://schema.org#>
         PREFIX ns4: <http://schema.mobivoc.org/>
         PREFIX ns5: <https://dbpedia.org/ontology/>
         PREFIX owl: <http://www.w3.org/2002/07/owl#>
         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

         SELECT DISTINCT ?district_name
         WHERE {
          ?parking ns1:hasDistrict ?district .
          ?district ns2:districtName ?district_name
          }
      """
)

q1_res = g.query(q1)

list_district = []
for row in q1_res:
    list_district.append(row.district_name)


# lista de los dropdown - TIPO DE PARKING
q2 = prepareQuery("""
         PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
         PREFIX ns2: <http://grupo12_open_data.org#>
         PREFIX ns3: <http://schema.org#>
         PREFIX ns4: <http://schema.mobivoc.org/>
         PREFIX ns5: <https://dbpedia.org/ontology/>
         PREFIX owl: <http://www.w3.org/2002/07/owl#>
         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

         SELECT DISTINCT ?additional_type
         WHERE {
          ?parking ns3:additionalType ?additional_type
          }
      """
)

q2_res = g.query(q2)

list_type_parking = []
for row in q2_res:
    list_type_parking.append(row.additional_type)


# lista de los latitudes
q3 = prepareQuery("""
         PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
         PREFIX ns2: <http://grupo12_open_data.org#>
         PREFIX ns3: <http://schema.org#>
         PREFIX ns4: <http://schema.mobivoc.org/>
         PREFIX ns5: <https://dbpedia.org/ontology/>
         PREFIX owl: <http://www.w3.org/2002/07/owl#>
         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

         SELECT DISTINCT ?coordinate
         WHERE {
          ?parking ns1:coordinate_location ?coordinate
          }
      """
)

#q3_res = g.query(q3)

#list_coordinates = []
#for row in q3_res:
#    list_coordinates.append(row.coordinate)

#APP
app.layout = html.Div([
    html.H1("🅿️ PARKINEO APP 🚗", style={'textAlign': 'center', 'background-color': '#D3D3D3', 'padding': '10px'}),
    dcc.Markdown('''### Please select the parking facility type: '''),
    dcc.RadioItems(
                id='radio-items-type-parking',
                options=['For residents','Public'],
                #options=[{'label': i, 'value': i} for i in list_type_parking],
                value='Public',
                labelStyle={'display': 'inline-block'}),
    html.Br(),
    html.Div(id='markdown-container'),
    html.Br(),
    html.Div(id='component-container', style={'margin-bottom': '20px'}),
    html.Br(),
    html.Div(id='table-container'),
    html.Br(),
    dcc.Graph(id='map-graph')
],style={'max-width': '800px', 'margin': 'auto'})

@app.callback(
    Output('markdown-container', 'children'),
    Input('radio-items-type-parking', 'value'))

def update_markdown(selected_option):
    if selected_option == 'Public':
        return dcc.Markdown('''### Please select the district:'''),[]
    else:
        return dcc.Markdown('''### Please select the price range: '''),[]

@app.callback(
    Output('component-container', 'children'),
    Input('radio-items-type-parking', 'value'))

def update_components(selected_option):
    if selected_option == 'Public':
        return dcc.Dropdown(id='district-dropdown',options=[{'label': x, 'value': x} for x in list_district], value=list_district[5]),[]
    
    else:
        return dcc.RangeSlider(id='price-slider',min=1000,max=25000,step=None,
                               marks={
                                   1000:'1.000€',
                                   5000:'5.000€',
                                   10000:'10.000€',
                                   15000:'15.000€',
                                   20000:'20.000€',
                                   25000:'25.000€',
                               },value=[1000, 25000]),[]
        




@app.callback(
    [
        Output('table-container', 'children', allow_duplicate=True),
        Output('map-graph', 'figure')
    ],
    [
        Input('district-dropdown', 'value'),  # Added an input for the selected district
       
    ],
    prevent_initial_call=True
)

def update_table(selected_district):
    #if selected_option == 'ROT':
        # Query to get parking names based on the selected district
    
    
    
    q4 = prepareQuery("""
        PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
        PREFIX ns2: <http://grupo12_open_data.org#>
        PREFIX ns3: <http://schema.org#>
        PREFIX ns4: <http://schema.mobivoc.org/>
        PREFIX ns5: <https://dbpedia.org/ontology/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?nameParking ?occupancy_value ?month
        WHERE {
        ?parking ns1:hasDistrict ?district .
        ?district ns2:districtName ?district_name .
        ?parking ns3:name ?nameParking .
        ?parking ns1:hasOccupancy ?occupancy .
        ?occupancy ns4:rateOfOccupancy ?occupancy_value .
        ?occupancy ns5:month ?month
        FILTER (?district_name = ?selected_district)
        }
    """)
    # Execute the query on the graph
    q4_res = g.query(q4, initBindings={'selected_district': Literal(selected_district)})
    dict_months={'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July',
                 '8':'August','9':'September','10':'October','11':'November','12':'December'}
    
    q6 = prepareQuery("""
        PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
        PREFIX ns2: <http://grupo12_open_data.org#>
        PREFIX ns3: <http://schema.org#>
        PREFIX ns4: <http://schema.mobivoc.org/>
        PREFIX ns5: <https://dbpedia.org/ontology/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?nameParking ?coordinate
        WHERE {
        ?parking ns3:name ?nameParking .
        ?parking ns1:coordinate_location ?coordinate .
        ?parking ns1:hasDistrict ?district .
        ?district ns2:districtName ?district_name .
        ?district ns2:districtName ?selected_district .
        FILTER(?selected_district)
                      
        }
    """)

    
    def assign_month_name(literal):
        month_number=literal[0]
        month_name=dict_months[month_number]
        return month_name
    
    

    q6_res = g.query(q6, initBindings={'selected_district':Literal(selected_district)})

    list_coordinates1 = []
    list_rot_parkings = []
    for row in q6_res:
        list_coordinates1.append(row.coordinate)
        list_rot_parkings.append(row.nameParking)

    #print(list_coordinates1)
    print(list_rot_parkings)

    #if len(list_coordinates1) == 0:
        # asignar valor random
        #list_coordinates1 = [Literal('45.4168,-7.7038')]
    #print(list_coordinates1)
    def parse_coordinates(literal):
        lat, lon = map(float, literal.value.split(','))
        return lat, lon
    
    coordinates=[]
    # Extraer las coordenadas para Plotly Express
    coordinates = [parse_coordinates(coord) for coord in list_coordinates1]
    print(coordinates)

    madrid_center = (40.4168, -3.7038)

    table_style = {
    'borderCollapse': 'collapse',
    'width': '100%',
    'border': '1px solid black',
    'margin-top': '10px',}

    # Create a table with the results
    table = html.Table(
    # Header
    [html.Tr([html.Th("Parking Name",style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'}),
               html.Th("Occupancy (%)",style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'}),
               html.Th("Month",style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'})],
               style={'background-color': '#ADD8E6', 'color': 'white'})] +
    # Body
    [html.Tr([html.Td(row.nameParking,style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'})
              , html.Td(row.occupancy_value,style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'}),
              html.Td(assign_month_name(row.month),style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'})]) for row in q4_res],
              style=table_style
    )
    
    # Crea un diccionario que asocie nombres de parkings con coordenadas
    data_dict_1 = {'nombreParking': list_rot_parkings, 'lat': [coord[0] for coord in coordinates], 'lon': [coord[1] for coord in coordinates]}

    # Crea un DataFrame a partir del diccionario (esto es opcional)
    # Puedes utilizar directamente el diccionario con px.scatter_mapbox
    import pandas as pd
    df1 = pd.DataFrame(data_dict_1)
    
    fig = px.scatter_mapbox(
        df1,
        lat='lat',  # Índice de latitud en la tupla de coordenadas
        lon='lon',  # Índice de longitud en la tupla de coordenadas
        title='Parkings en Madrid',
        hover_name='nombreParking',
        zoom=10,
        center=dict(lon=madrid_center[1], lat=madrid_center[0]),
        color_discrete_sequence=['red'],  # Establece el color a rojo
        
    )
    fig.update_layout(mapbox_style="open-street-map")  # Utiliza el estilo de mapa de OpenStreetMap
    return table, fig
    




@app.callback(
    [
    Output('table-container', 'children', allow_duplicate=True),
    Output('map-graph', 'figure', allow_duplicate=True)
    ],
    [
    Input('price-slider', 'value'),  # Added an input for the selected district
    ],
    prevent_initial_call=True
)

def update_table_price(selected_price):
    

    #PRICE SPECIFICATION -- AVERAGE PRICE PARKING
    q5 = prepareQuery("""
        PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
        PREFIX ns2: <http://grupo12_open_data.org#>
        PREFIX ns3: <http://schema.org#>
        PREFIX ns4: <http://schema.mobivoc.org/>
        PREFIX ns5: <https://dbpedia.org/ontology/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?nameParking ?averagePrice_parking
        WHERE {
        ?parking ns3:name ?nameParking .
        ?parking ns2:average_price ?averagePrice_parking .
        FILTER (?averagePrice_parking >= ?price_min && ?averagePrice_parking <= ?price_max)
        }
    """)
         
    # Execute the query on the graph
    q5_res = g.query(q5, initBindings={'price_min': Literal(selected_price[0]), 'price_max': Literal(selected_price[1])}) 
   
    #for row in q5_res:
      #return row
      

    #COORDENADAS MAPA
    q7 = prepareQuery("""
        PREFIX ns1: <http://grupo12_open_data.es/lcc/resource#>
        PREFIX ns2: <http://grupo12_open_data.org#>
        PREFIX ns3: <http://schema.org#>
        PREFIX ns4: <http://schema.mobivoc.org/>
        PREFIX ns5: <https://dbpedia.org/ontology/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?nameParking ?coordinate
        WHERE {
        ?parking ns1:coordinate_location ?coordinate .
        ?parking ns3:name ?nameParking .
        ?parking ns2:average_price ?averagePrice_parking .
        FILTER (?averagePrice_parking >= ?price_min && ?averagePrice_parking <= ?price_max)
                      
        }
    """)
    q7_res = g.query(q7, initBindings={'price_min': Literal(selected_price[0]), 'price_max': Literal(selected_price[1])})

    list_coordinates2 = []
    list_priv_parkings = []
    for row in q7_res:
        list_coordinates2.append(row.coordinate)
        list_priv_parkings.append(row.nameParking)
    
    #print(list_coordinates2)

    def parse_coordinates(literal):
        lat, lon= map(float, literal.value.split(','))
        return lat, lon

    # Extraer las coordenadas para Plotly Express
    coordinates2 = [parse_coordinates(coord) for coord in list_coordinates2]

    madrid_center = (40.4168, -3.7038)

    table_style = {
    'borderCollapse': 'collapse',
    'width': '100%',
    'border': '1px solid black',
    'margin-top': '10px',
}
    
    # Create a table with the results
    table = html.Table(
    # Header
    [html.Tr([html.Th("Parking Name",style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'}),
               html.Th("Average Price",style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'})],
               style={'background-color': '#ADD8E6', 'color': 'white'})] +
    # Body
    [html.Tr([html.Td(row.nameParking,style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'}),
               html.Td(row.averagePrice_parking,style={'padding-top':'2px', 'padding-bottom':'2px','text-align':'center'})]) for row in q5_res],
               style=table_style
    )
    
    # Crea un diccionario que asocie nombres de parkings con coordenadas
    data_dict = {'nombreParking': list_priv_parkings, 'lat': [coord[0] for coord in coordinates2], 'lon': [coord[1] for coord in coordinates2]}

    # Crea un DataFrame a partir del diccionario (esto es opcional)
    # Puedes utilizar directamente el diccionario con px.scatter_mapbox
    import pandas as pd
    df = pd.DataFrame(data_dict)


    fig = px.scatter_mapbox(
        df,
        lat='lat',  # Índice de latitud en la tupla de coordenadas
        lon='lon',  # Índice de longitud en la tupla de coordenadas
        title='Parkings en Madrid',
        hover_name='nombreParking',
        center=dict(lon=madrid_center[1], lat=madrid_center[0]),
        color_discrete_sequence=['red'],  # Establece el color a rojo
        
    )
    fig.update_layout(mapbox_style="open-street-map")  # Utiliza el estilo de mapa de OpenStreetMap

    return table, fig



if __name__ == '__main__':
    app.run_server(debug=True)
