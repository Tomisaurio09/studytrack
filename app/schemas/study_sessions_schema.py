from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import datetime

class StudySessionsSchema(Schema):
    subject_id = fields.Int(required=True)
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)
    subject_id = fields.Int(required=True)

    @validates("start_time")
    def validate_start(self, value, **kwargs):
        try:
            datetime.strptime(value, "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")

    @validates("end_time")
    def validate_end(self, value, **kwargs):
        try:
            datetime.strptime(value, "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")
    
    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start = datetime.strptime(data["start_time"], "%I:%M%p")
        end = datetime.strptime(data["end_time"], "%I:%M%p")

        if end <= start:
            raise ValidationError({"end_time": "La hora de salida debe ser posterior a la de entrada"})



class EditStudySessionsSchema(Schema):
    start_time = fields.Str(required=True)
    end_time = fields.Str(required=True)
    subject_id = fields.Int(required=True)

    @validates("start_time")
    def validate_start(self, value, **kwargs):
        try:
            datetime.strptime(value, "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")

    @validates("end_time")
    def validate_end(self, value, **kwargs):
        try:
            datetime.strptime(value, "%I:%M%p")
        except ValueError:
            raise ValidationError("El formato debe ser HH:MMAM/PM, por ejemplo 03:00PM")

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start = datetime.strptime(data["start_time"], "%I:%M%p")
        end = datetime.strptime(data["end_time"], "%I:%M%p")

        if end <= start:
            raise ValidationError({"end_time": "La hora de salida debe ser posterior a la de entrada"})
