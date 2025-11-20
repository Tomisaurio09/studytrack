from marshmallow import Schema, fields, validates, ValidationError

class SubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    total_hours_goal = fields.Int(required=True)
    total_hours_completed = fields.Int(required=False, load_default=0)
    priority_level = fields.Str(required=True)
    status = fields.Str(required=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value) > 100:
            raise ValidationError("El nombre de la materia debe tener como máximo 100 caracteres.")
        
    @validates("description")
    def validate_description(self, value, **kwargs):
        if len(value) > 512:
            raise ValidationError("La descripción de la materia debe tener como máximo 512 caracteres.")

    @validates("total_hours_goal")
    def validate_hours_goal(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours goal must be non-negative.")


class EditSubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    total_hours_goal = fields.Int(required=True)
    total_hours_completed = fields.Int(required=True)
    priority_level = fields.Str(required=True)
    status = fields.Str(required=True)

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