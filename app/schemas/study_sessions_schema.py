from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class StudySessionsSchema(Schema):
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)

    @validates("start_time")
    @validates("end_time")
    def validate_times(self, data, **kwargs):
        try:
            # Parseamos con formato de 12 horas (ej: 03:00PM)
            start = datetime.strptime(data["start_time"], "%I:%M%p")
            end = datetime.strptime(data["end_time"], "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")

        # Validamos que la hora de salida sea posterior a la de entrada
        if end <= start:
            raise ValidationError("La hora de salida debe ser posterior a la de entrada")

class EditStudySessionsSchema(Schema):
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)

    @validates("start_time")
    @validates("end_time")
    def validate_times(self, data, **kwargs):
        try:
            # Parseamos con formato de 12 horas (ej: 03:00PM)
            start = datetime.strptime(data["start_time"], "%I:%M%p")
            end = datetime.strptime(data["end_time"], "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")

        # Validamos que la hora de salida sea posterior a la de entrada
        if end <= start:
            raise ValidationError("La hora de salida debe ser posterior a la de entrada")