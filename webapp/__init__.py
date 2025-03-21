from typing import Any
from flask import Flask, render_template, request
import os
import json
from webapp.form_generator import generate_form_fields


app = Flask(__name__, static_folder = '../static')
app.config['UPLOAD_FOLDER'] = 'static/thumbs'

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
        with open(f'data/{entity_type}/template.json') as f:
            template = json.load(f)
        return render_template('dashboard.html', entity_type=entity_type, title=template.get("title", entity_type))

    entities = [json.loads(entity) for entity in request.args.getlist("entities")]
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