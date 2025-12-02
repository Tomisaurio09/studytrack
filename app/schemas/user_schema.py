from marshmallow import Schema, fields, validates, validates_schema, ValidationError, pre_load, post_load
import bleach
import re

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)
    
    @pre_load
    def sanitize_input(self, data, **kwargs):
        text_fields = ["username", "email"] 
        for field in text_fields:
            if field in data and isinstance(data[field], str):
                data[field] = bleach.clean( data[field], tags=[],strip=True ) 
        return data

    @validates("username")
    def validate_username(self, value, **kwargs):
        # Solo letras y números
        if not re.match(r"^[A-Za-z0-9]+$", value):
            raise ValidationError("The username must contain only letters and numbers.")

        # Al menos una letra y un número
        if not (re.search(r"[A-Za-z]", value) and re.search(r"[0-9]", value)):
            raise ValidationError("The username must include both letters and numbers.")

        # Longitud máxima
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
        
    #optional
    @post_load
    def final_cleanup(self, data, **kwargs):
        if "username" in data:
            data["username"] = data["username"].strip()
        return data

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @pre_load
    def sanitize_input(self, data, **kwargs):
        if "username" in data:
            data["username"] = bleach.clean(data["username"], tags=[], strip=True)
        return data


