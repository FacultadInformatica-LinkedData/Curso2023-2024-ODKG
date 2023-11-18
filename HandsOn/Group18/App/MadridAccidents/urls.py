from django.contrib import admin
from django.urls import path
from Ontology_Web_App.views import ListOntologies, SparqlQueryAPIView, SparqlQueryHTMLView , homeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', homeView, name='redirect_to_sparql_query'),

    # API views
    path('api/ontologies/', ListOntologies.as_view(), name='list_ontologies_api'),
    

    # HTML views (with query_type)
    path('sparql_query/<int:ontology_id>/<str:query_type>/', SparqlQueryHTMLView.as_view(), name='sparql_query_html_view_with_type'),

    # HTML views (without query_type)
    path('sparql_query/<int:ontology_id>/', SparqlQueryHTMLView.as_view(), name='sparql_query_html_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

