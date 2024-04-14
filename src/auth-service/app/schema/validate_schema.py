from marshmallow import Schema, fields


class ValidateSchema(Schema):
    """
    Schema for validating the presence of an access token.

    Fields:
    --------
    access_token : str
        Required. The JWT access token to be validated.
    """
    access_token = fields.String(
        required=True,
        error_messages={
            "required": "Access token is required."
        }
    )
