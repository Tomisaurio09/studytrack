from marshmallow import Schema, fields, validates, validates_schema, ValidationError, pre_load, post_load
import bleach
from datetime import datetime

class StudySessionsSchema(Schema):
    subject_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)   
    end_time = fields.DateTime(required=True)
    notes = fields.Str(required=False, load_default="")
    #you can pass 03:00PM as the hour format
    @pre_load
    def parse_hour_minute(self, data, **kwargs):
        for field in ["start_time", "end_time"]:
            if field in data and isinstance(data[field], str):
                today = datetime.today().date()
                try:
                    # Try AM/PM format
                    parsed_time = datetime.strptime(data[field].strip(), "%I:%M%p").time()
                except ValueError:
                    try:
                        # Try 24-hour format
                        parsed_time = datetime.strptime(data[field].strip(), "%H:%M").time()
                    except ValueError:
                        raise ValidationError({field: "Invalid time format"})
                data[field] = datetime.combine(today, parsed_time).isoformat()
        return data

    
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
    
    @post_load
    def final_cleanup(self, data, **kwargs):
        text_fields = ["notes"] 
        for field in text_fields:
            if field in data:
                data[field] = data[field].strip()
        return data



class EditStudySessionsSchema(Schema):
    start_time = fields.DateTime(required=True)   
    end_time = fields.DateTime(required=True)
    subject_id = fields.Int(required=True)
    notes = fields.Str(required=False, load_default="")

    @pre_load
    def parse_hour_minute(self, data, **kwargs):
        for field in ["start_time", "end_time"]:
            if field in data and isinstance(data[field], str):
                today = datetime.today().date()
                try:
                    # Try AM/PM format
                    parsed_time = datetime.strptime(data[field].strip(), "%I:%M%p").time()
                except ValueError:
                    try:
                        # Try 24-hour format
                        parsed_time = datetime.strptime(data[field].strip(), "%H:%M").time()
                    except ValueError:
                        raise ValidationError({field: "Invalid time format"})
                data[field] = datetime.combine(today, parsed_time).isoformat()
        return data

    
    @pre_load
    def sanitize_input(self, data, **kwargs):
        text_fields = ["notes"] 
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                data[field] = bleach.clean( data[field], tags=[],strip=True ) 
        return data
    
    @post_load
    def final_cleanup(self, data, **kwargs):
        text_fields = ["notes"] 
        for field in text_fields:
            if field in data:
                data[field] = data[field].strip()
        return data

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        start = data["start_time"]
        end = data["end_time"]

        if end <= start:
            raise ValidationError({"end_time": "The end time must be later than the start time"})
        