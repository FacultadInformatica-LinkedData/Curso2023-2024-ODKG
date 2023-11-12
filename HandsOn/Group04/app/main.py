from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Cargar el archivo .ttl al grafo RDF
graph = Graph()
graph.parse("./output-datasets-with-links-updated.ttl", format="turtle")
ns = Namespace("http://www.madculturalevents.es/group04/ontology/madculturalevents#")
schema = Namespace("http://schema.org/")

@app.route('/')
def home():
    query = """
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX schema: <http://schema.org/> 
    SELECT ?name ?eventPrice ?eventAccessibility ?eventPlace WHERE {
      ?event a schema:Event ;
               schema:name ?name ;
               ns0:price ?eventPrice ;
               ns0:accesibility ?eventAccessibility ;
               ns0:hasPlace ?eventPlace  .
    }
    """
    result = execute_sparql_query(query)
    prices = get_prices()
    accessibilities = get_accessibilities()
    districts = get_districts()
    return render_template('index.html', query=query, result=result, prices=prices, accessibilities=accessibilities,
                           districts=districts)

def execute_sparql_query(query):
    results = graph.query(query)

    result_values = []
    for row in results:
        result_row = []
        for value in row:
            result_row.append(value.toPython() if hasattr(value, 'toPython') else value)
        result_values.append(result_row)

    return result_values

def get_prices():
    query = '''
    SELECT DISTINCT ?price
    WHERE {
        ?event a schema:Event ;
            ns:price ?price .
    }
    '''
    # Almacena los resultados en una lista
    prices_list = [row.price for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

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
    districts_list = [row.district for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

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
    accessibility_list = [row.accessibility for row in graph.query(query, initNs={"ns": ns, "schema": schema})]

    # Combina todas las cadenas en una sola
    combined_accessibility = ",".join(accessibility_list)

    # Divide la cadena combinada en elementos únicos
    unique_accessibility = set(combined_accessibility.split(','))

    # Visualiza los resultados
    print("Accessibility:", list(unique_accessibility))
    return list(unique_accessibility)

@app.route('/search')
def search():
    search_value = request.args.get('search_value', '')
    q1 = f"""
    PREFIX ns0: <http://www.madculturalevents.es/group04/ontology/madculturalevents#>
    PREFIX schema: <http://schema.org/> 

    SELECT ?name ?eventPrice ?eventAccessibility ?eventPlace WHERE {{
        ?event a schema:Event .
        ?event schema:name ?name .
        ?event ns0:price ?eventPrice .
        ?event ns0:accesibility ?eventAccessibility .
        ?event ns0:hasPlace ?eventPlace .
        FILTER (CONTAINS(?name, "{search_value}"))
    }}
    """
    result = execute_sparql_query(q1)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)