
from PIL import Image
import io
import uuid
import os

def process_image(file_stream) -> str:
    img = Image.open(io.BytesIO(file_stream.read()))
    img.thumbnail((300, 300))
    thumb_path = os.path.join("static/thumbs", f"thumb_{uuid.uuid4()}.jpg")
    img.save(thumb_path)
    return f"/{thumb_path}"


# Missing Piece 3: Default Values
def apply_defaults(template):
    defaults = {}
    for field, config in template["properties"].items():
        if "default" in config:
            defaults[field] = config["default"]
    return defaults


def normalize_type(raw_type: str, format: str = "") -> str:
    if raw_type == "string":
        if format == "uri":
            return "file"
    return raw_type


def generate_form_fields(template):
    fields = []
    required_fields = template.get("required", [])
    for key, config in template["properties"].items():
        items = config.get("items")
        field = {
            "key": key,
            "label": config.get("description", key),
            "type": normalize_type(config.get("type", "unsupported"), config.get("format", "")),
            "required": key in required_fields,
            "default": config.get("default", None),
            "items_type": normalize_type(items.get("type", "unsupported"), items.get("format", "")) if items is not None else None,
            "pattern": config.get("pattern", None),
        }

        fields.append(field)
    return fields