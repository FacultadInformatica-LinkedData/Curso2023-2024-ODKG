from flask_marshmallow import Schema
from marshmallow.fields import Str


class LocalSchema(Schema):
    """
    Class schema to export the information in AnswerModel in proper way.
    """

    class Meta:
        # Fields to expose
        local = ["local"]
        sameAsNombreDistrito = ["sameAsNombreDistrito"]
        lat = ["lat"]
        long = ["long"]
        horaCierre = ["horaCierre"]
        horaApertura = ["horaApertura"]
        rotulo = ["rotulo"]
        situacion = ["situacion"]
        mesas = ["mesas"]
        sillas = ["sillas"]
        superficie = ["superficie"]

    local = Str()
    sameAsNombreDistrito = Str()
    lat = Str()
    long = Str()
    horaCierre = Str()
    horaApertura = Str()
    rotulo = Str()
    situacion = Str()
    mesas = Str()
    sillas = Str()
    superficie = Str()
