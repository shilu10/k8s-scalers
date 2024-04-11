from marshmallow import Schema, fields, validate, ValidationError


class PreSignedUrlSchema(Schema):
    filename = fields.String(required=True, 
                            validate=validate.Length(min=5), 
                            error_messages={"invalid": "video filename must be an string."})
    
    filesize = fields.Integer(required=True, 
                              error_messages={"invalid": "video filesize must be an integer and required."})