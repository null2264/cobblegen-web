# Bare Minimum Framework

## For Backend Developers Who Aren't Paid to Make UI but Need Something Better than CLI

## What is it?

Bare Minimum Framework is exactly what it sounds like - the absolute bare minimum interface for managing JSON data without touching the command line. It automatically generates CRUD interfaces from simple template files, allowing you to create, read, update, and delete structured data with zero frontend development.

## Why Does This Exist?

Because sometimes you just need a simple interface to manipulate data without the headache of building a UI. Perfect for:

- Building proof-of-concept applications
- Managing configuration for simple apps
- Administering Discord bots or other automation tools
- Quick internal tools where functionality trumps aesthetics
- When "good enough" is actually good enough

## How It Works

The framework reads a folder structure containing JSON templates and data files, then automatically generates a minimalist interface for manipulating that data:

EXAMPLE

```
/data/
├── channels/
│   ├── template.json  # Defines structure and form fields
│   ├── channel_a.json
│   └── channel_b.json
├── characters/
│   ├── template.json
│   ├── character_a.json
│   └── character_b.json
```

Each subfolder in the `/data` directory represents a different "object type" that can be managed through the dashboard. The `template.json` file in each folder defines the structure and editable fields for that object type.

## Features

- **Zero UI Development**: No HTML, CSS, or frontend code to write
- **Auto-Generated Forms**: Creates appropriate form elements based on data types
- **String Manipulation**: Edit any string-like object within JSON
- **Image Link Rendering**: Preview and update image links
- **Full CRUD Operations**: Create, read, update, and delete JSON objects
- **Instant Setup**: Point it at a folder and you're good to go
- **No Database Required**: Works directly with the file system

## Getting Started

1. Install the package:
   ```
   pip install -r requirements.txt
   ```

2. Create your data folder structure with template files:
   ```
   /data/
   └── your-object-type/
       └── template.json
   ```

3. Start the server:
   ```
   flask --app webapp.app run
   ```

4. Navigate to `http://localhost:5000` and start managing your data

## Template Format

The `template.json` file uses a simple format to define editable fields:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "path": "data", 
    "fields": {
      "avatar": {
        "type": "string",
        "format": "uri",
        "description": "Character avatar (URL)"
      },
      "name": {
        "type": "string",
        "minLength": 1
      },
      "description": { "type": "string" },
      "personality": { "type": "string" },
      "creator_notes": { "type": "string" }
    },
    "required": ["avatar", "name"]
  }
```

## Limitations

- No authentication or user management (if you need those,  you're using the wrong tool)
- Limited field types and customization (literally only works with string, will add int and float support)
- Not designed for high-volume data (will add standard database reader)
- No relational data support (same as above)
- Simple, functional UI with zero frills 

## Who Should Use This?

- Backend developers who hate CSS
- Solo developers building internal tools
- Anyone who needs a quick admin interface
- People who value function over form
- Developers who think "it's just a config panel, why am I spending days on this?"

## License

MIT

## Contributing

Pull requests welcome. The bar is intentionally low - it's called "Bare Minimum" for a reason.
