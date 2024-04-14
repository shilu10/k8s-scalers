from marshmallow import Schema, fields, validate, ValidationError


class LoginSchema(Schema):
    """
    Schema for validating user login input.

    Fields:
    --------
    email : str
        Required. Must be a valid email format.
        
    password : str
        Required. Must be a string between 6 and 128 characters.
    """
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format."
        }
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={
            "required": "Password is required."
        }
    )
