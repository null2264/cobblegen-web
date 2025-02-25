
from jsonschema import validate, ValidationError


def validate_data(data, template):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            template["path"]: {  # Dynamic path-aware schema
                "type": "object",
                "properties": template["fields"],
                "required": template.get("required", [])
            }
        },
        "required": [template["path"]] if template.get("path") else []
    }
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid data at {e.json_path}: {e.message}")