from django.urls import path
from . import views

urlpatterns = [
    path('listar-puntos-desfibrilador/', views.listar_puntos_desfibrilador, name='listar-puntos-desfibrilador'),
    path('listar-municipalidades/', views.listar_municipalidades, name='listar-municipalidades'),
    path('listar-tipos-placeType/', views.listar_tipos_placeType, name='listar-tipos-placeType'),

]
