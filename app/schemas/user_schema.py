from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates("username")
    def validate_username(self, value, **kwargs):
        if not value.isalpha():
            raise ValidationError("El nombre solo debe contener letras.")
        if len(value) > 15:
            raise ValidationError("El username debe tener como máximo 15 caracteres.")

    @validates("password")
    def validate_password_length(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError("Las contraseñas no coinciden", field_name="confirm_password")


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class SubjectSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    total_hours_goal = fields.Int(required=True)
    total_hours_completed = fields.Int(required=False, load_default=0)
    priority_level = fields.Str(required=True)
    status = fields.Str(required=True)

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

    @validates("total_hours_goal")
    def validate_hours_goal(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours goal must be non-negative.")

    @validates("total_hours_completed")
    def validate_hours_completed(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Total hours completed must be non-negative.")
