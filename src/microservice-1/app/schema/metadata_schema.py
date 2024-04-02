from marshmallow import Schema, fields, validate, ValidationError

class MetadataSchema(Schema):
    title = fields.String(required=True, 
                            validate=validate.Length(min=5), 
                            error_messages={"invalid": "video title must be an string."})
    
    description = fields.String(required=True, 
                            validate=validate.Length(min=10), 
                            error_messages={"invalid": "video description must be an string."})
