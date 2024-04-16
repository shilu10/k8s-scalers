from marshmallow import Schema, fields, validate, ValidationError


class PartSchema(Schema):
    part_number = fields.Int(required=True)
    etag = fields.Str(required=True)


class MultiPartCompleteSchema(Schema):
    """
    Schema to validate the structure of the multipart completion request.

    This schema ensures the request body contains:
    - `filename`: The name of the video file being uploaded.
    - `uploadID`: A unique identifier for the upload session.
    - `parts`: A list containing information about the uploaded file parts.

    Attributes:
        filename (str): The filename of the video being uploaded.
        uploadID (str): The unique identifier for the upload.
        parts (list): A list of uploaded parts for the video.

    Validation Rules:
    - `filename`: Must be a string and have a minimum length of 5 characters.
    - `uploadID`: Must be a string and have a minimum length of 5 characters.
    - `parts`: Must be a list and cannot be empty.

    Error Handling:
    - If `filename` or `uploadID` does not meet the minimum length requirement, a custom error message will be raised.
    - The `parts` field must be provided and cannot be empty.
    """
    filename = fields.String(
        required=True, 
        validate=validate.Length(min=5), 
        error_messages={
            "required": "Filename is required.",
            "invalid": "Video filename must be a string with a minimum length of 5 characters."
        }
    )
    
    uploadID = fields.String(
        required=True, 
        validate=validate.Length(min=5),
        error_messages={
            "required": "Upload ID is required.",
            "invalid": "Upload ID must be a string with a minimum length of 5 characters."
        }
    )

    parts = fields.List(fields.Nested(PartSchema), required=True, 
        validate=validate.Length(min=1),  # Ensures the list has at least one item.
        error_messages={
            "required": "Parts information is required.",
            "invalid": "Parts must be provided as a list with at least one part."
        })
