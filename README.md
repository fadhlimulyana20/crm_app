# FastAPI MVC Starter Project

This is a starter project using FastAPI with Jinja2 templates, structured in MVC architecture.

## Features

- Hello World web page at `/`
- Hello World API endpoint at `/api/hello`
- Customer CRUD API endpoints:
  - POST `/customers/` - Create customer
  - GET `/customers/{id}` - Get customer by ID
  - GET `/customers/` - List customers
  - PUT `/customers/{id}` - Update customer
  - DELETE `/customers/{id}` - Delete customer

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python run.py
   ```

3. Open your browser to `http://127.0.0.1:8000` for the web page.
   API at `http://127.0.0.1:8000/api/hello`
   API docs at `http://127.0.0.1:8000/docs`

## Structure

- `app/models/`: Data models (SQLAlchemy)
- `app/views/`: (Reserved for future views)
- `app/controllers/`: Route handlers
- `app/templates/`: Jinja2 templates
- `app/static/`: Static files
- `app/database.py`: Database configuration