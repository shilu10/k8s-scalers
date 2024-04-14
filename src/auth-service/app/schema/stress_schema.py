from marshmallow import Schema, fields, validate, ValidationError


class CPUStressSchema(Schema):
    """
    Schema for validating CPU stress test parameters.

    Validates:
    - 'load': Required CPU load percentage (20–95)
    - 'duration': Required test duration in seconds (10–120)
    - 'workers': Optional number of CPU stress workers (0–24)
    """
    load = fields.Integer(
        required=True,
        validate=validate.Range(min=20, max=95),
        error_messages={
            "required": "CPU load is required.",
            "invalid": "Load must be an integer.",
            "validator_failed": "Load must be between 20 and 95."
        }
    )

    duration = fields.Integer(
        required=True,
        validate=validate.Range(min=10, max=120),
        error_messages={
            "required": "Duration is required.",
            "invalid": "Duration must be an integer.",
            "validator_failed": "Duration must be between 10 and 120 seconds."
        }
    )

    workers = fields.Integer(
        required=False,
        validate=validate.Range(min=0, max=24),
        error_messages={
            "invalid": "Workers must be an integer.",
            "validator_failed": "Workers must be between 0 and 24."
        }
    )


class MemoryStressSchema(Schema):
    """
    Schema for validating memory stress test parameters.

    Validates:
    - 'mem_bytes': Required memory amount as string (e.g. '512M', '2G')
    - 'duration': Required test duration in seconds (10–120)
    - 'vm_workers': Required number of memory stress workers (1–20)
    """
    mem_bytes = fields.String(
        required=True,
        error_messages={
            "required": "Memory size is required.",
            "invalid": "Memory size must be a string (e.g., '512M')."
        }
    )

    duration = fields.Integer(
        required=True,
        validate=validate.Range(min=10, max=120),
        error_messages={
            "required": "Duration is required.",
            "invalid": "Duration must be an integer.",
            "validator_failed": "Duration must be between 10 and 120 seconds."
        }
    )

    vm_workers = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=20),
        error_messages={
            "required": "VM workers is required.",
            "invalid": "VM workers must be an integer.",
            "validator_failed": "VM workers must be between 1 and 20."
        }
    )


class MemoryAndCpuStressSchema(Schema):
    """
    Schema for validating combined CPU and memory stress test parameters.

    Validates:
    - 'mem_bytes': Required memory string
    - 'load': Required CPU load percentage (20–95)
    - 'duration': Required duration (10–120)
    - 'workers': Optional CPU workers (0–24)
    - 'vm_workers': Required memory workers (1–20)
    """
    mem_bytes = fields.String(
        required=True,
        error_messages={
            "required": "Memory size is required.",
            "invalid": "Memory size must be a string (e.g., '512M')."
        }
    )

    load = fields.Integer(
        required=True,
        validate=validate.Range(min=20, max=95),
        error_messages={
            "required": "CPU load is required.",
            "invalid": "Load must be an integer.",
            "validator_failed": "Load must be between 20 and 95."
        }
    )

    duration = fields.Integer(
        required=True,
        validate=validate.Range(min=10, max=120),
        error_messages={
            "required": "Duration is required.",
            "invalid": "Duration must be an integer.",
            "validator_failed": "Duration must be between 10 and 120 seconds."
        }
    )

    workers = fields.Integer(
        required=False,
        validate=validate.Range(min=0, max=24),
        error_messages={
            "invalid": "Workers must be an integer.",
            "validator_failed": "Workers must be between 0 and 24."
        }
    )

    vm_workers = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=20),
        error_messages={
            "required": "VM workers is required.",
            "invalid": "VM workers must be an integer.",
            "validator_failed": "VM workers must be between 1 and 20."
        }
    )


# Schema instances for actual validation use
cpu_stress_schema = CPUStressSchema()
mem_stress_schema = MemoryStressSchema()
cpu_mem_stress_schema = MemoryAndCpuStressSchema()
