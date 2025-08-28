# TravelBook — Travel Booking Application (Django)

A simple travel booking web app built with Django. Users can register/login, browse travel options (flight/train/bus), book seats, view/cancel bookings, and manage their profile.

## Features
- Django auth: registration, login, logout, profile update
- Travel options model with type, source, destination, datetime, price, available seats
- Booking flow with seat validation and atomic seat decrement
- My bookings page with cancel option (seats returned)
- Filtering by type, source, destination, date, and text search
- Responsive Bootstrap UI
- Unit tests for critical paths
- MySQL support via PyMySQL (or SQLite fallback for quick start)

## Quickstart (Local)

1) Create and activate a virtual environment, then install deps:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) (Optional) Configure **MySQL** by copying `.env.example` to `.env` and filling the MYSQL_* values.  
If you skip this, SQLite will be used automatically.

3) Run migrations and create a superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4) Load sample travel options (optional):
```bash
python manage.py loaddata core/fixtures/travel_options.json
```

5) Start the dev server:
```bash
python manage.py runserver
```

Login at `/admin` to add more travel options, or use the UI at `/travels/`.

## Running Tests
```bash
pytest
```

## Deployment (PythonAnywhere quick path)
- Create a new PythonAnywhere app, upload this project, set up a virtualenv, and install `requirements.txt`.
- Set environment variables (SECRET_KEY, ALLOWED_HOSTS, and optional MYSQL_* if you have a MySQL DB).
- Point the WSGI file to `travelbook.wsgi` and reload.
- For DB, you may deploy SQLite for demo or use a hosted MySQL (PlanetScale/RDS). Run `python manage.py migrate` on the console.

## Security & Validation
- Password validators enabled; CSRF protection and server-side seat checks.
- Seat operations are **transactional** with row locks to prevent overselling.
