from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Cargar el archivo .ttl al grafo RDF
g = Graph()
g.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")

@app.route('/')
def home():
    query = """PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    SELECT ?event ?eventPrice ?eventAccessibility ?eventPlace WHERE {
        ?event a ns0:CulturalEvent ;
               ns0:price ?eventPrice ;
               ns0:accesibility ?eventAccessibility ;
               ns0:hasPlace ?eventPlace  .
    } """
    result = execute_sparql_query(query)
    prices = get_prices()
    accessibilities = get_accessibilities()
    districts = get_districts()
    return render_template('index.html', query=query, result=result, prices=prices, accessibilities=accessibilities,
                           districts=districts)

@app.route('/sparql', methods=['POST'])
def sparql_query():
    query = request.form['query']
    result = execute_sparql_query(query)
    return render_template('./sparql.html', query=query, result=result)




def get_prices():
    query = '''
    SELECT DISTINCT ?price
    WHERE {
        ?event a schema:Event ;
            ns:price ?price .
    }
    '''
    # Almacena los resultados en una lista
    prices_list = [row.price for row in g.query(query, initNs={"ns": ns, "schema": schema})]

    # Visualiza los resultados
    print("Precios:", prices_list)
    return prices_list


def get_districts():
    query = '''
    SELECT DISTINCT ?district
    WHERE {
        ?address a ns:Address ;
               ns:belongsTo ?district ;
      }
    '''
    # Almacena los resultados en una lista
    districts_list = [row.district for row in g.query(query, initNs={"ns": ns, "schema": schema})]

    # Visualiza los resultados
    print("Districts:", districts_list)
    return districts_list

def get_accessibilities():
    query = '''
    SELECT DISTINCT ?accessibility
    WHERE {
        ?event a schema:Event ;
            ns:accesibility ?accessibility .
    }
    '''
    # Almacena los resultados en una lista
    accessibility_list = [row.accessibility for row in g.query(query, initNs={"ns": ns, "schema": schema})]

    # Combina todas las cadenas en una sola
    combined_accessibility = ",".join(accessibility_list)

    # Divide la cadena combinada en elementos únicos
    unique_accessibility = set(combined_accessibility.split(','))

    # Visualiza los resultados
    print("Accessibility:", list(unique_accessibility))
    return list(unique_accessibility)


def execute_sparql_query(query):
    results = g.query(query)

    # Obtener los valores reales de los objetos
    result_values = []
    for row in results:
        result_row = []
        for value in row:
            # Convertir objetos RDF a valores de Python
            result_row.append(value.toPython() if hasattr(value, 'toPython') else value)
        result_values.append(result_row)
    return result_values

if __name__ == '__main__':
    app.run(debug=True)
