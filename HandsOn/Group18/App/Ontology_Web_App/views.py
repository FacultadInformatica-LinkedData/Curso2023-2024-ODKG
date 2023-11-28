
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from .models import Ontology
from .serializers import OntologySerializer
from rdflib import Graph,Namespace, Literal
from django.conf import settings
from rest_framework.views import APIView
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS
from rest_framework.renderers import TemplateHTMLRenderer
from django.views import View



class ListOntologies(generics.ListCreateAPIView):
    queryset = Ontology.objects.all()
    serializer_class = OntologySerializer


class SparqlQueryAPIView(APIView):
    def get(self, request, ontology_id,query_type=None):
        try:
            ontology = Ontology.objects.get(pk=ontology_id)
            query_results = self.execute_sparql_query(ontology, sparql_query)

            return Response({"data": query_results})
        except Ontology.DoesNotExist:
            return Response({"error": "Ontology not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def execute_sparql_query(self, ontology, sparql_query):
        g = settings.ONTOLOGY_GRAPH

        if g is None:
            return {"error": "Ontology graph not loaded"}

        try:
            results = g.query(sparql_query)
            serialized_results = [row for row in results]
            return serialized_results
        except Exception as e:
            print(f"Error executing SPARQL query: {str(e)}")
            return {"error": f"Error executing SPARQL query: {str(e)}"}

class SparqlQueryHTMLView(APIView):
    def get(self, request, ontology_id,query_type=None):
        try:
            ontology = Ontology.objects.get(pk=ontology_id)

            if query_type==None:
                return render(request, 'error_message.html', {'message': 'Se requiere un tipo de consulta específico.'})
            
            
            #build Sparql Query based on Query type parameter
            sparql_query = self.construct_sparql_query(query_type)

            query_results = self.execute_sparql_query(ontology, sparql_query)

            print("Query Results:", query_results) 

            #include image path

            image_path = self.get_image_path(query_type)
            print("Path:",image_path)
            context = {'query_results': query_results, 'image_path': image_path,'District':query_type}

            return render(request, 'sparql_results.html', context)
        except Ontology.DoesNotExist:
            return Response({"error": "Ontology not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


    def construct_sparql_query(self, query_type):
        # Construir el SPARQL query en función del valor de query_type
        ns = Namespace("http://MadridTransit.com/")
        vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
        owl = Namespace("http://www.w3.org/2002/07/owl#")
        rdf = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        nso = Namespace("http://MadridTransit.com/ontology/")
        dbp = Namespace("https://dbpedia.org/ontology/")
        prot = Namespace("http://www.ontotext.com/proton/protonext#")
  
        
        
        q1="""
                SELECT (COUNT(?addr) AS ?accidentCount)
                WHERE {
                        ?district a dbp:District;
                        nso:name "%s";
                        nso:districtCode ?dc.    
                        ?addr nso:belongsDistrict ?district.
                        }
                """ % query_type
        
        q2= """
                SELECT ?population ?area
                WHERE {
                        ?district a dbp:District;
                        nso:name "%s";
                        nso:districtCode ?districtCode;
                        wdo:P1082 ?population;
                        wdo:P2046 ?area.
                }
                """ % query_type

        q3="""
                SELECT ?area
                WHERE {
                        ?district a dbp:District;
                        nso:name "%s";
                        nso:districtCode ?districtCode;
                        wdo:P2046 ?area.
                }
                """ % query_type

        q4="""
                SELECT (COUNT(?accidente) AS ?accidentCount)
                WHERE {
                        ?accidente a prot:Accident.
                }
                """ 


        

        
        queries=[q1,q2,q3,q4]

        return queries



    def execute_sparql_query(self, ontology, sparql_query):
        g = settings.ONTOLOGY_GRAPH
        print("Sparql:", sparql_query)

        if g is None:
            return {"error": "Ontology graph not loaded"}

        try:
            serialized_results=[]

            for i in sparql_query:
                result= g.query(i)
                serialized_result = [ r for r in result]
                #print("Serialized Results:", serialized_result)
                print("Prueba2:", serialized_result[0][0])
                #print("Type:", type(serialized_result[0][0]))
                serialized_results.append(serialized_result[0][0])


##            results = g.query(sparql_query)
##            serialized_results = [ r for r in results]
##            print("Serialized Results:", serialized_results)
##            print("pruba1:",serialized_results[0])
##            print("Prueba2:", serialized_results[0][0])
            serialized_results[0]= int(serialized_results[0])
            serialized_results[1]= int(serialized_results[1])
            serialized_results[2]= float(serialized_results[2])
            serialized_results[2]= round(serialized_results[2],2)
            serialized_results[3]= int(serialized_results[3])
            percapita=round(float(serialized_results[0]/serialized_results[1]),4)
            densidad= round(float(serialized_results[0]/serialized_results[2]),4)
            x=float(serialized_results[0])
            y=float(serialized_results[3])
            percentage=(x/y)*100
            percentage= round(percentage,2)
            serialized_results.append(percapita)
            serialized_results.append(densidad)
            serialized_results.append(percentage)
            return serialized_results
        except Exception as e:
            print(f"Error executing SPARQL query: {str(e)}")
            return {"error": f"Error executing SPARQL query: {str(e)}"}

    def get_image_path(self, query_type):
        # Define the image paths based on query_type
        image_paths = {
            'Centro': '/media/Distritos/Centro.png',
            'Arganzuela': '/media/Distritos/Arganzuela.png',
            'Retiro': '/media/Distritos/Retiro.png',
            'Salamanca': '/media/Distritos/Salamanca.png',
            'Chamartin': '/media/Distritos/Chamartin.png',
            'Tetuan': '/media/Distritos/Tetuan.png',
            'Chamberi': '/media/Distritos/Chamberi.png',
            'Fuencarral': '/media/Distritos/Fuencarral_El_Pardo.png',
            'Moncloa-Aravaca': '/media/Distritos/Moncloa_Aravaca.png',
            'Latina': '/media/Distritos/Latina.png',
            'Carabanchel': '/media/Distritos/Carabanchel.png',
            'Usera': '/media/Distritos/Usera.png',
            'Moratalaz': '/media/Distritos/Moratalaz.png',
            'Hortaleza': '/media/Distritos/Hortaleza.png',
            'Villaverde': '/media/Distritos/Villaverde.png',
            'Vicalvaro': '/media/Distritos/Vicalvaro.png',
            'Barajas': '/media/Distritos/Barajas.png',




            # Add more paths as needed
        }

        # Return the image path for the given query_type
        return image_paths.get(query_type, 'default_image.jpg')



def homeView(request):
    if request.method == 'POST':
        query = request.POST.get('q', '')  # Obtener el valor del formulario
        # Realizar alguna validación si es necesario

        # Redirigir a la página de búsqueda con la consulta en la URL
        return redirect(f'/sparql_query/1/{query}/')

    return render(request, 'index.html')

