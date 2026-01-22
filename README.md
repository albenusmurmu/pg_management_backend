# PG Management Backend

Django REST API backend for PG (Paying Guest) Management System.

## Tech Stack
- Django
- Django REST Framework
- SimpleJWT (JWT Authentication)
- SQLite (development)
- Python-dotenv

## Features
- JWT-based authentication (access & refresh tokens)
- Token blacklist & rotation
- Role-based API access
- PG management (rooms, tenants, bills, facilities)

## Setup Instructions

```bash
git clone https://github.com/albenusmurmu/pg_management_backend.git
cd pg_management_backend/pg_managementPRD
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
