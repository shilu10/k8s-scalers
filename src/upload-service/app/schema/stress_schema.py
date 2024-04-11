from marshmallow import Schema, fields, validate, ValidationError


class CPUStressSchema(Schema):
    load = fields.Integer(required=True, 
                        validate=validate.Range(min=20, max=95), 
                        error_messages={"invalid": "load must be an integer and between 20 to 95."}
                    )
    
    duration = fields.Integer(required=True, 
                            validate=validate.Range(min=10, max=120), 
                            error_messages={"invalid": "duration must be an integer and between 10 to 120."}
                        )
    
    workers = fields.Integer(required=False,
                            validate=validate.Range(min=0, max=24),
                            error_messages={"invalid": "workers must be an integer and between 0 to 24."}
                        )
    

class MemoryStressSchema(Schema):
    mem_bytes = fields.String(required=True)
    
    duration = fields.Integer(required=True, 
                            validate=validate.Range(min=10, max=120), 
                            error_messages={"invalid": "duration must be an integer and between 10 to 120."}
                        )
    

class MemoryAndCpuStressSchema(Schema):
    mem_bytes = fields.String(required=True)

    load = fields.Integer(required=True, 
                        validate=validate.Range(min=20, max=95), 
                        error_messages={"invalid": "load must be an integer and between 20 to 95."}
                    )
    
    duration = fields.Integer(required=True, 
                            validate=validate.Range(min=10, max=120), 
                            error_messages={"invalid": "duration must be an integer and between 10 to 120."}
                        )
    
    workers = fields.Integer(required=False,
                            validate=validate.Range(min=0, max=24),
                            error_messages={"invalid": "workers must be an integer and between 0 to 24."}
                        )


cpu_stress_schema = CPUStressSchema()
mem_stress_schema = MemoryStressSchema()
cpu_mem_stress_schema = MemoryAndCpuStressSchema()