from marshmallow import Schema, fields, validate, ValidationError

class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required.", "invalid": "Invalid email format."}
    )
    
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        error_messages={"required": "Password is required."}
    )
