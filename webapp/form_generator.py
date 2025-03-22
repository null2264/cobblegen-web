
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


def generate_form_fields(template):
    fields = []
    for field, config in template["properties"].items():
        type_ = config.get("type", "unsupported")
        if type_ == "string":
            format = config.get("format", "")
            if format == "uri":
                type_ = "file"

        fields.append({
            "key": field,
            "label": config.get("description", field),
            "type": type_,
            "required": config.get("required", False),
            "default": config.get("default", None),
        })
    return fields