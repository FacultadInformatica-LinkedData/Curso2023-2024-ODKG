from flask_marshmallow import Schema
from marshmallow.fields import Nested, List
from api.schema.local_schema import LocalSchema


class LocalesSchema(Schema):
    """
    Class schema to export the information in AnswerModel in proper way.
    """

    class Meta:
        # Fields to expose
        locales = ["locales"]

    locales = List(Nested(LocalSchema))
