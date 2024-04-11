from marshmallow import Schema, fields, validate, ValidationError


class CaptionSchema(Schema):
    video_url = fields.String(
        required=True,
        error_messages={"required": "Video url is required", "invalid": "Invalid video url."}
    )
