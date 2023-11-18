from django.apps import AppConfig
from django.conf import settings


class OntologyLoadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ontology_load'
    def ready(self):
        # Cargar la ontología al iniciar la aplicación
        if settings.ONTOLOGY_GRAPH == None:
            from rdflib import Graph
            print ("Cargando ontología")
            ontology_path = 'DjangoOntology/media/ontologies/final3.ttl'
            ontology_graph = Graph()
            ontology_graph.parse(ontology_path, format="turtle")
            settings.ONTOLOGY_GRAPH = ontology_graph
            print("ontologia Cargada")
        else:
            print('ontology already loaded')

    



