from marshmallow import Schema, fields, validate, ValidationError


class CaptionSchema(Schema):
    """
    Schema for validating caption generation requests.

    Fields:
        video_url (str): Required URL string pointing to the video resource.
    """
    video_url = fields.String(
        required=True,
        validate=validate.Length(min=5),  # Optional: basic length check
        error_messages={
            "required": "Video url is required",
            "invalid": "Invalid video url.",
        }
    )
