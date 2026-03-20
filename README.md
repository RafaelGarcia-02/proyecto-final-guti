# Pyramid CRUD App

A simple CRUD application built with Pyramid, SQLAlchemy, and Jinja2 templates, with user authentication.

## Features

- User registration and login/logout
- Create, Read, Update, Delete items (protected for logged-in users)
- SQLite database
- Basic HTML frontend

## Setup

1. Install dependencies:
   pip install -e .

2. Run the development server:
   python -m pyramid.scripts.pserve development.ini

3. Open http://localhost:6543 in your browser.

## Usage

- Register a new account or login with existing credentials.
- Once logged in, you can manage items (add, edit, delete).
- Logout to end the session.

## Structure

- `myapp/` - Application package
- `myapp/models.py` - SQLAlchemy models (Item and User)
- `myapp/views.py` - Pyramid views
- `myapp/templates/` - Jinja2 templates
- `myapp/static/` - Static files
- `development.ini` - Configuration