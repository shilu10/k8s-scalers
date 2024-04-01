from marshmallow import Schema, fields, validate, ValidationError

class MessageSchema(Schema):
    message = fields.String(required=True, 
                            validate=validate.Length(min=10), 
                            error_messages={"invalid": "message must be an string."})
