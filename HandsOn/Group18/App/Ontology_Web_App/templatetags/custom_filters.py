from django import template
from rdflib import URIRef, Literal, BNode

register = template.Library()

@register.filter
def get_class_name(value):
    return value.__class__.__name__




