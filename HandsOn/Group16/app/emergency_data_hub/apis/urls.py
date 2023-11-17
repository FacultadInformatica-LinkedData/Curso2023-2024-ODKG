from django.urls import path
from . import views

urlpatterns = [
    path('listar-puntos-desfibrilador/', views.listar_desfibriladores, name='listar-puntos-desfibrilador'),
    path('listar-municipalidades/', views.listar_municipalidades, name='listar-municipalidades'),
    path('listar-tipos-placeType/', views.listar_tipos_placeType, name='listar-tipos-placeType'),
    path('generate/', views.generate_rdf, name='generate_rdf'),
    path('generate_ttl/', views.generate_ttl_from_nt, name='generate_rdf'),

]
