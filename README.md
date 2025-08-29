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
Assignment compliance (what’s implemented)

Backend

✅ Registration / Login / Logout via Django auth.

✅ Profile update page for name/email/password (see /profile/).

✅ Models

TravelOption: code (Travel ID), travel_type (Flight/Train/Bus), source, destination, departure_at, price, seats (available seats).

Booking: booking_code, user, travel, seat_count, total, booked_at, status (Confirmed/Cancelled).

✅ Booking flow with validation:

Prevents over-booking (atomic transaction + seat checks).

Computes total = seat_count * price.

✅ Manage bookings:

“My bookings” page with current & past bookings.

Cancel booking (returns seats back to inventory).

Frontend

✅ Templates for home, register/login, profile, travel list (with filters & search), booking form, and bookings list.

✅ Responsive UI via Bootstrap 5 (+ static/css/travelbook.css).

Bonus / Extras

✅ Filters & search: by type, source, destination, date, and free-text.

✅ MySQL ready (see .env instructions).

✅ Unit tests for bookings, cancellations, and filters (see core/tests.py).

URLs

/ (home), /register/, /login/, /logout/, /profile/

/travels/ (list + filters), /travels/<pk>/ (detail + booking form)

/bookings/ (list), /bookings/<pk>/cancel/ (cancel)

/admin/ (admin)

How to deploy to PythonAnywhere (quick)

Sign in → “Start a new web app” → “Manual configuration” → Python 3.x.

On the Consoles tab: start a Bash console.

Clone your repo:

git clone https://github.com/vasavi2015/TravelBook.git
cd TravelBook


Create a virtualenv & install deps:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Environment: create .env (use .env.example as reference).
For first deploy, simplest is SQLite:

DEBUG=False
SECRET_KEY=<generate_a_strong_value>
ALLOWED_HOSTS=<your-username>.pythonanywhere.com
DB_ENGINE=sqlite
DB_NAME=db.sqlite3


Migrate & collect static:

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser   # optional


Web tab → edit WSGI config: point project path to your repo folder and ensure:

import os, sys
path = '/home/<your-username>/TravelBook'
if path not in sys.path: sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelbook.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

In the Web tab, set Working directory to the repo root, and Virtualenv to /home/<user>/TravelBook/.venv.

Static files mapping (Web tab):

URL: /static/ → Folder: /home/<user>/TravelBook/static/

Reload the app (big green button).
Your URL will be: https://<your-username>.pythonanywhere.com

Using MySQL on PythonAnywhere (bonus):

Create a MySQL database from the “Databases” tab.

Put the DB credentials in .env:

DB_ENGINE=mysql
DB_NAME=<pa-username>$<db-name>
DB_USER=<pa-username>
DB_PASSWORD=<your-db-password>
DB_HOST=<pa-username>.mysql.pythonanywhere-services.com
DB_PORT=3306


pip install mysqlclient (already in requirements if you added it).

Run python manage.py migrate.
