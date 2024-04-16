from marshmallow import Schema, fields, validate


class PreSignedUrlSchema(Schema):
    """
    Schema for validating input parameters required to generate pre-signed S3 URLs.

    Fields:
    - filename: Name of the file to upload (must be a string, at least 5 characters).
    - filesize: Size of the file in bytes (must be a positive integer).
    """

    filename = fields.String(
        required=True,
        validate=validate.Length(min=5),
        error_messages={
            "required": "Filename is required.",
            "invalid": "Filename must be a string.",
            "validator_failed": "Filename must be at least 5 characters long."
        }
    )

    filesize = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Filesize is required.",
            "invalid": "Filesize must be an integer.",
            "validator_failed": "Filesize must be greater than 0."
        }
    )
