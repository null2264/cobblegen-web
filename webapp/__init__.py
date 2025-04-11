from typing import Any
from flask import Flask, render_template, request
from pathlib import Path
import copy
import os
import json
from webapp.form_generator import generate_form_fields, normalize_type


app = Flask(__name__, static_folder = '../static')

def is_htmx() -> bool:
    return request.headers.get("HX-Request", type=bool) or False

def get_entities() -> list[Any]:
    entities = []
    for data in os.listdir('data'):
        if not os.path.isdir(f'data/{data}'):
            continue

        with open(f'data/{data}/template.json') as f:
            template = json.load(f)

        entities.append({ "name": data, "title": template.get("title", data) })
    return entities

# --------------------------
# Route: Home Dashboard (Entity Types)
# --------------------------
@app.route('/')
def home():
    return render_template('home.html', entities=get_entities())

# --------------------------
# Route: Entity Type Dashboard
# --------------------------
@app.route('/<entity_type>')
def entity_dashboard(entity_type):
    if not is_htmx():
        template_path = Path(f"data/{entity_type}/template.json")
        if not template_path.exists():
            return app.send_static_file(entity_type)

        with template_path.open("r") as f:
            template = json.load(f)
        return render_template('dashboard.html', entity_type=entity_type, title=template.get("title", entity_type))

    entities_json = request.args.get("entities")
    entities = json.loads(entities_json) if entities_json else {}
    return render_template('dashboard_partial.html', entity_type=entity_type, entities=entities)

# --------------------------
# Route: Edit Entity
# --------------------------
@app.route('/<entity_type>/<entity_name>/edit')
def edit_entity(entity_type, entity_name):
    # Load template
    with open(f'data/{entity_type}/template.json') as f:
        template = json.load(f)

    if not is_htmx():
        return render_template('form.html',
                             entity_type=entity_type,
                             entity_name=entity_name,
                             fields=generate_form_fields(template),
                             title=template.get("title", entity_type),
                             data={})

    entity_json = request.args.get("entity")
    entity = json.loads(entity_json) if entity_json else {}
    return render_template('form_partial.html',
                         entity_type=entity_type,
                         entity_name=entity_name,
                         fields=generate_form_fields(template),
                         title=template.get("title", entity_type),
                         data=entity)

# --------------------------
# Route: Create Entity
# --------------------------
@app.route('/<entity_type>/create')
def create_entity(entity_type):
    # Load template
    with open(f'data/{entity_type}/template.json') as f:
        template = json.load(f)

    if not is_htmx():
        return render_template('form.html',
                             entity_type=entity_type,
                             entity_name="",
                             fields=generate_form_fields(template),
                             title=template.get("title", entity_type),
                             data={})

    return render_template('form_partial.html',
                         entity_type=entity_type,
                         entity_name="",
                         fields=generate_form_fields(template),
                         title=template.get("title", entity_type),
                         data={})

@app.route('/<entity_type>/form_array_partial/<key>')
def form_array_partial(entity_type, key):
    with open(f'data/{entity_type}/template.json') as f:
        template = json.load(f)

    config = template["properties"][key].get("items")

    return render_template(
        'form_partial_partial.html',
        entity_type=entity_type,
        key=key,
        type=normalize_type(config.get("type", "unsupported")),
        default=None,
        options=[],
        is_required=True,
    )

@app.route('/modal/export')
def export_modal():
    data_json = request.args.get("data")
    data = json.loads(data_json) if data_json else {}
    v1_0 = copy.deepcopy(data)
    v1_0["customGen"] = {}
    v1_0["formatVersion"] = "1.0"
    for k, v in v1_0.items():
        if not Path(f"data/{k}/").exists():
            continue

        for gen in v:
            if not gen.get("modifier"):
                continue

            v.remove(gen)
            modifier = gen["modifier"]
            del gen["modifier"]

            if k not in v1_0["customGen"]:
                v1_0["customGen"][k] = {}

            if modifier not in v1_0["customGen"][k]:
                v1_0["customGen"][k][modifier] = []

            v1_0["customGen"][k][modifier].append(gen)
    v1_1 = copy.deepcopy(data)
    v1_1["formatVersion"] = "1.1"
    return render_template('export_modal.html', v1_0=json.dumps(v1_0, indent=4), v1_1=json.dumps(v1_1, indent=4))

@app.errorhandler(404)
def four_o_four(_):
    return render_template("404.html"), 404