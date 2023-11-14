from flask_marshmallow import Schema
from marshmallow.fields import List, Str


class DistritoSchema(Schema):
    """
    Class schema to export the information in the street endpoint in proper way.
    """

    class Meta:
        # Fields to expose
        nombres = ["nombres"]

    nombres = List(Str())
