from django.core.management.base import BaseCommand
from rdflib import Graph
from django.conf import settings

class Command(BaseCommand):
    help = 'Load and parse the ontology from the media folder'

    def handle(self, *args, **options):
        # Replace with the relative path to your ontology file in the media folder
        ontology_path = 'DjangoOntology/media/ontologies/Accidents_linked_ultra_mega_Final_Siuuuu.ttl'

        # Create an RDF graph and parse the ontology
        ontology_graph = Graph()
        ontology_graph.parse(ontology_path, format="turtle")
        settings.ONTOLOGY_GRAPH = ontology_graph
        print(ontology_graph)
        print("2")
        print(settings.ONTOLOGY_GRAPH)

        self.stdout.write(self.style.SUCCESS('Ontology loaded successfully'))

