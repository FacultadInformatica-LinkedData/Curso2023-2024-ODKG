from rest_framework.serializers import ModelSerializer
from .models import Ontology

class OntologySerializer(ModelSerializer):
    class Meta:
        model = Ontology
        fields = '__all__'


