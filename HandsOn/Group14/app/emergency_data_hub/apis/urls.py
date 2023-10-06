from django.urls import path
from . import views

urlpatterns = [
    path('example-json/', views.example, name='example-json'),
    path('politicians/', views.politicians, name='politicians'),
]