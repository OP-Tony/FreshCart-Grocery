# FreshCart Grocery

A zero-cost Django grocery delivery MVP for a college project submission. It supports customer registration, product browsing, cart, checkout, simulated payment, delivery slots, order history, and admin inventory/order management.

## Project Overview
Based on the project's [Problem Statement](file:///C:/Users/TONY/Downloads/UpSkill-project/Problem%20Statement.txt), this application is designed for a department store management system:
- **Inventory & Cataloging**: All grocery items are listed with real-time quantities and pricing.
- **Customer Journey**: Users can register/login, browse products, add items to their cart, select preferred delivery slots, and proceed to checkout.
- **Simulated Transactions**: Features a mock payment page supporting various payment options.
- **Fulfillment & Administration**: Tracks delivery slots and provides dashboard access for admin inventory/order processing.


## Tech Stack

- Python 3.13
- Django 5.2
- SQLite for free PythonAnywhere deployment
- Optional MySQL for local development
- Django templates and CSS

## Local Setup

```powershell
cd "C:\Users\TONY\Downloads\Unstop-project\Grocery Store"
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000`.

Demo accounts after seeding:

- Admin: `admin` / `admin123`
- Customer: `customer` / `customer123`

## Optional Local MySQL

Create `.env` from `.env.example` and set:

```env
DB_MODE=mysql
MYSQL_DATABASE=grocery_store
MYSQL_USER=root
MYSQL_PASSWORD=your-local-password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Create the database in MySQL, then run migrations:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_demo
```

## Free PythonAnywhere Deployment

Use the free Beginner account and deploy with SQLite.

1. Push this folder to a free GitHub repository.
2. Create a PythonAnywhere free account.
3. Clone the repository in a PythonAnywhere Bash console.
4. Create a virtualenv and install requirements.
5. Run migrations and seed data.
6. Configure the WSGI file to point to `grocery_store.settings`.
7. Configure static files:
   - URL: `/static/`
   - Path: `/home/yourusername/project/staticfiles`
8. Run `python manage.py collectstatic`.
9. Reload the web app.

Final URL format: `https://yourusername.pythonanywhere.com`.

## Docker

Docker is optional for sharing the full local MySQL setup:

```powershell
docker compose up --build
```

Then run migrations inside the web container.
