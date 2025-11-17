from marshmallow import Schema, fields, validates, validates_schema, ValidationError

class SubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()

    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value) > 100:
            raise ValidationError("El nombre de la materia debe tener como máximo 100 caracteres.")
        
    @validates("description")
    def validate_description(self, value, **kwargs):
        if len(value) > 512:
            raise ValidationError("La descripción de la materia debe tener como máximo 512 caracteres.")

class EditSubjectSchema(Schema):
    name = fields.Str()
    description = fields.Str()

    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value) > 100:
            raise ValidationError("El nombre de la materia debe tener como máximo 100 caracteres.")
        
    @validates("description")
    def validate_description(self, value, **kwargs):
        if len(value) > 512:
            raise ValidationError("La descripción de la materia debe tener como máximo 512 caracteres.")