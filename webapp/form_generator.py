
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
    for field, config in template["fields"].items():
        if "default" in config:
            defaults[field] = config["default"]
    return defaults


def generate_form_fields(template):
    path = template.get("path", "")  # "data" → "data.whatever.thing"
    fields = []
    for field, config in template["fields"].items():
        full_key = f"{path}.{field}" if path else field  # "data.avatar"
        fields.append({
            "key": full_key,
            "label": config.get("description", field),
            "type": "file" if "uri" in config.get("format", "") else "text"
        })
    return fields

# Later in your CRUD routes:
def nest_data(flat_data, path_separator="."):
    nested = {}
    for key, value in flat_data.items():
        parts = key.split(path_separator)
        current = nested
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value
    return nested