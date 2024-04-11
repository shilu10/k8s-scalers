from marshmallow import Schema, fields, validate, ValidationError


class MetadataSchema(Schema):
    filename = fields.String(required=True, 
                            validate=validate.Length(min=5), 
                            error_messages={"invalid": "video filename must be an string."})
    
