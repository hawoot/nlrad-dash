# NLRAD Dashboard

A modular Voila-based dashboard with access control, nested widget groups, and a modern landing page.

## Features

- **Fast Landing Page**: Displays widget cards without loading any widget code
- **Independent Widgets**: Each widget runs in its own kernel (complete isolation)
- **Nested Groups**: Organize widgets in multi-level hierarchies
- **Access Control**: Role-based permissions with user-specific overrides
- **Modern UI**: Bootstrap-styled cards with responsive grid layout

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with Voila

```bash
voila landing/landing_page.ipynb --template=nlrad
```

Or run the entire dashboard:

```bash
voila . --template=nlrad
```

### 3. Access the Dashboard

Open your browser to: `http://localhost:8866/voila/render/landing/landing_page.ipynb`

## Project Structure

```
nlrad-dash/
├── config/
│   └── dashboard_config.json   # Groups, widgets, and access control
├── landing/
│   └── landing_page.ipynb      # Main landing page
├── widgets/                     # Your widget notebooks
│   ├── analytics/
│   ├── data_entry/
│   └── admin/
├── src/                         # Python modules
│   ├── config_loader.py        # Configuration parser
│   ├── access_control.py       # Permission checking
│   └── user_detection.py       # User detection (stub)
├── templates/nlrad/             # Custom Voila template
├── voila.json                   # Voila configuration
└── requirements.txt             # Python dependencies
```

## Configuration

Edit `config/dashboard_config.json` to customize:

### Adding a Widget

Add a widget inside a group's `widgets` array:

```json
{
  "id": "my_widget",
  "name": "My Widget",
  "description": "Description here",
  "path": "widgets/category/my_widget.ipynb",
  "icon": "chart-line",
  "permissions": ["category.view"]
}
```

### Creating Groups

Groups can be nested to any depth:

```json
{
  "id": "parent_group",
  "name": "Parent Group",
  "icon": "folder",
  "groups": [
    {
      "id": "child_group",
      "name": "Child Group",
      "widgets": [...]
    }
  ],
  "widgets": [...]
}
```

### Managing Access

Define roles and assign them to users:

```json
{
  "access_control": {
    "roles": {
      "admin": {
        "permissions": ["analytics.view", "admin.manage"]
      }
    },
    "users": {
      "alice": {
        "roles": ["admin"]
      }
    }
  }
}
```

## User Detection

Edit `src/user_detection.py` to implement your authentication:

```python
def get_current_user() -> str:
    # Example: Read from JupyterHub
    import os
    return os.environ.get('JUPYTERHUB_USER', 'anonymous')
```

## Icons

Widget and group icons use [Font Awesome 5](https://fontawesome.com/v5/search?m=free).
Use the icon name without the `fa-` prefix (e.g., `chart-bar`, `users`, `cog`).

## Creating New Widgets

1. Create a new `.ipynb` file in the appropriate `widgets/` subdirectory
2. Add the widget to `config/dashboard_config.json` in the desired group
3. Set the required permissions

Each widget is completely independent and can use any libraries you need.
