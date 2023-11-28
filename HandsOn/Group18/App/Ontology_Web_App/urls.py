from django.contrib import admin
from django.urls import path
from Ontology_Web_App.views import ListOntologies, SparqlQueryView

urlpatterns = [
    path('list/', ListOntologies.as_view(), name='list-ontologies'),
    path('sparql/<int:ontology_id>/', SparqlQueryView.as_view(), name='sparql-query'),
]
