from marshmallow import Schema, fields, validates, validates_schema, ValidationError, pre_load, post_load
import bleach

class SubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    total_hours_goal = fields.Int(required=True)
    total_hours_completed = fields.Int(required=False, load_default=0)
    priority_level = fields.Str(required=True)
    status = fields.Str(required=True)

    @pre_load
    def sanitize_input(self, data, **kwargs):
        text_fields = ["name", "description", "priority_level", "status"] 
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                data[field] = bleach.clean( data[field], tags=[],strip=True ) 
        return data
    
    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value) > 100:
            raise ValidationError("The name of the subject must be at most 100 characters long.")
        
    @validates("description")
    def validate_description(self, value, **kwargs):
        if len(value) > 512:
            raise ValidationError("The description of the subject must be at most 512 characters long.")

    @validates("total_hours_goal")
    def validate_hours_goal(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours goal must be non-negative.")
    
    @post_load
    def final_cleanup(self, data, **kwargs):
        text_fields = ["name", "description", "priority_level", "status"] 
        for field in text_fields:
            if field in data:
                data[field] = data[field].strip()
        return data

class EditSubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    total_hours_goal = fields.Int(required=True)
    total_hours_completed = fields.Int(required=True)
    priority_level = fields.Str(required=True)
    status = fields.Str(required=True)

    @pre_load
    def sanitize_input(self, data, **kwargs):
        text_fields = ["name", "description", "priority_level", "status"] 
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                data[field] = bleach.clean( data[field], tags=[],strip=True ) 
        return data
    
    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value) > 100:
            raise ValidationError("The name of the subject must be at most 100 characters long.")
        
    @validates("description")
    def validate_description(self, value, **kwargs):
        if len(value) > 512:
            raise ValidationError("The description of the subject must be at most 512 characters long.")

    @validates("total_hours_goal")
    def validate_hours_goal(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours goal must be non-negative.")

    @validates("total_hours_completed")
    def validate_hours_completed(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours completed must be non-negative.")

    @post_load
    def final_cleanup(self, data, **kwargs):
        text_fields = ["name", "description", "priority_level", "status"] 
        for field in text_fields:
            if field in data:
                data[field] = data[field].strip()
        return data