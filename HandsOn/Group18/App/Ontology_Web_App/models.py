from django.db import models

class Ontology(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='ontologies/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
