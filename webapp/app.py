
from flask import Flask, render_template, request, redirect, url_for
import os
import json
from webapp.form_generator import generate_form_fields, nest_data
app = Flask(__name__, static_folder = '../static')
app.config['UPLOAD_FOLDER'] = 'static/thumbs'
import uuid
# --------------------------
# Route: Home Dashboard (Entity Types)
# --------------------------
@app.route('/')
def home():
    entities = [d for d in os.listdir('data') if os.path.isdir(f'data/{d}')]
    return render_template('home.html', entities=entities)

# --------------------------
# Route: Entity Type Dashboard
# --------------------------
@app.route('/<entity_type>')
def entity_dashboard(entity_type):
    entities = []
    entity_dir = f'data/{entity_type}'
    if os.path.exists(entity_dir):
        for f in os.listdir(entity_dir):
            if f.endswith('.json') and f != 'template.json':
                with open(f'{entity_dir}/{f}') as file:
                    data = json.load(file)
                    entities.append({
                        'name': os.path.splitext(f)[0],
                        'avatar': data.get('data', {}).get('avatar', ''),
                        'description': data.get('data', {}).get('description', '')
                    })
    return render_template('dashboard.html', entity_type=entity_type, entities=entities)

# --------------------------
# Route: Delete Entity
# --------------------------
@app.route('/<entity_type>/<entity_name>/delete', methods=['POST'])
def delete_entity(entity_type, entity_name):
    target = f'data/{entity_type}/{entity_name}.json'
    if os.path.exists(target):
        os.remove(target)
    return redirect(url_for('entity_dashboard', entity_type=entity_type))

# --------------------------
# Route: Edit Entity
# --------------------------
@app.route('/<entity_type>/<entity_name>/edit')
def edit_entity(entity_type, entity_name):
    # Load template
    with open(f'data/{entity_type}/template.json') as f:
        template = json.load(f)

    # Load existing data if editing
    existing_data = {}
    if entity_name:
        with open(f'data/{entity_type}/{entity_name}.json') as f:
            existing_data = json.load(f)

    return render_template('edit_form.html',
                         entity_type=entity_type,
                         entity_name=entity_name,
                         fields=generate_form_fields(template),
                         data=existing_data)

# --------------------------
# Route: Create Entity
# --------------------------
@app.route('/<entity_type>/create')
def create_entity(entity_type):
    # Load template
    with open(f'data/{entity_type}/template.json') as f:
        template = json.load(f)

    return render_template('edit_form.html',
                         entity_type=entity_type,
                         entity_name="",
                         fields=generate_form_fields(template),
                         data={})


# --------------------------
# Routes: Handle Form Submissions
# --------------------------

# Route for updating existing entities
@app.route('/<entity_type>/<entity_name>/update', methods=['POST'])
def update_entity(entity_type, entity_name):
    # 1. Flatten form data
    flat_data = {k: v for k, v in request.form.items()}

    # 2. Handle image uploads separately
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename:
            # Save to uploads, process thumbnail
            filename = f"{uuid.uuid4()}_{file.filename}"
            thumb_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Ensure the upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(thumb_path)
            # Update the data with the path
            flat_data[file_key] = f"/static/thumbs/{filename}"

    # 3. Convert flat keys to nested structure
    nested_data = nest_data(flat_data)

    # 4. Save as JSON
    with open(f'data/{entity_type}/{entity_name}.json', 'w') as f:
        json.dump(nested_data, f)
    
    return redirect(url_for('entity_dashboard', entity_type=entity_type))

# Route for creating new entities
@app.route('/<entity_type>/save', methods=['POST'])
def save_new_entity(entity_type):
    # 1. Flatten form data
    flat_data = {k: v for k, v in request.form.items()}

    # 2. Handle image uploads separately
    for file_key in request.files:
        file = request.files[file_key]
        if file.filename:
            # Save to uploads, process thumbnail
            filename = f"{uuid.uuid4()}_{file.filename}"
            thumb_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Ensure the upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(thumb_path)
            # Update the data with the path
            flat_data[file_key] = f"/static/thumbs/{filename}"

    # 3. Convert flat keys to nested structure
    nested_data = nest_data(flat_data)

    # 4. Save as JSON with a new UUID
    new_filename = f"{uuid.uuid4()}.json"
    with open(f'data/{entity_type}/{new_filename}', 'w') as f:
        json.dump(nested_data, f)
    
    return redirect(url_for('entity_dashboard', entity_type=entity_type))
