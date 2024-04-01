from marshmallow import Schema, fields, validate, ValidationError


class StressSchema(Schema):
    stress_amount = fields.Integer(required=True, 
                                  validate=validate.Range(min=20, max=95), 
                                  error_messages={"invalid": "stress_amount must be an integer and between 20 to 95."})
    
    stress_timeout = fields.Integer(required=True, 
                                   validate=validate.Range(min=10, max=120), 
                                   error_messages={"invalid": "stress_timeout must be an integer and between 10 to 120."})