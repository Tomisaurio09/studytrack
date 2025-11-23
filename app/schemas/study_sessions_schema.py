from marshmallow import Schema, fields, validates, validates_schema, ValidationError, pre_load
import bleach
from datetime import datetime

class StudySessionsSchema(Schema):
    subject_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)   
    end_time = fields.DateTime(required=True)

    @pre_load
    def parse_hour_minute(self, data, **kwargs):
        for field in ["start_time", "end_time"]:
            if field in data and isinstance(data[field], str):
                today = datetime.today().date()
                parsed_time = datetime.strptime(data[field], "%I:%M%p").time()
                data[field] = datetime.combine(today, parsed_time).isoformat()
        return data

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start = data["start_time"]
        end = data["end_time"]

        if end <= start:
            raise ValidationError({"end_time": "The end time must be later than the start time"})




class EditStudySessionsSchema(Schema):
    start_time = fields.DateTime(required=True)   
    end_time = fields.DateTime(required=True)
    subject_id = fields.Int(required=True)

    @pre_load
    def parse_hour_minute(self, data, **kwargs):
        for field in ["start_time", "end_time"]:
            if field in data and isinstance(data[field], str):
                today = datetime.today().date()
                parsed_time = datetime.strptime(data[field], "%I:%M%p").time()
                data[field] = datetime.combine(today, parsed_time).isoformat()
        return data

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start = data["start_time"]
        end = data["end_time"]

        if end <= start:
            raise ValidationError({"end_time": "The end time must be later than the start time"})
        