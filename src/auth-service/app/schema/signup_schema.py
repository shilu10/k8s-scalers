from marshmallow import Schema, fields, validate, ValidationError


class SignUpSchema(Schema):
    """
    Schema for validating user signup input.

    Fields:
    --------
    email : str
        Required. Must be a valid email address.

    password : str
        Required. Must be a string between 6 and 128 characters.
        Optional: Can be extended with custom validators for strength (e.g., digits, uppercase).
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

    # Optional: custom validator for even stronger password rules
    # Uncomment if you want
    # @validates("password")
    # def validate_password_strength(self, value):
    #     if not any(c.isdigit() for c in value):
    #         raise ValidationError("Password must contain at least one digit.")
    #     if not any(c.isupper() for c in value):
    #         raise ValidationError("Password must contain at least one uppercase letter.")
