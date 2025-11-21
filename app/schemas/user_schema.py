from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates("username")
    def validate_username(self, value, **kwargs):
        if not value.isalpha():
            raise ValidationError("The name must contain only letters.")
        if len(value) > 15:
            raise ValidationError("The username must be at most 15 characters long.")

    @validates("password")
    def validate_password_length(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
        
    @validates("password")
    def validate_password_complexity(self, value, **kwargs):
        if value.isalpha() or value.isdigit():
            raise ValidationError("The password must be a combination of letters and numbers.")

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError("The passwords do not match", field_name="confirm_password")


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)



