from marshmallow import Schema, fields, validate, ValidationError


class ValidateSchema(Schema):
    access_token = fields.String(
        required=True,
        error_messages={"required": "Access Token"}
    )
    
    
