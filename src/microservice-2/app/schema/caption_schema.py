from marshmallow import Schema, fields, validate, ValidationError


class CaptionSchema(Schema):
    video_url = fields.String(
        required=True,
        error_messages={"required": "Video url is required", "invalid": "Invalid video url."}
    )
    
    language = fields.String(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={"required": "language is required."}
    )
