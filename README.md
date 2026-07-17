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
- SQLite (default database)
- Optional MySQL for local development
- Django templates and CSS

## Local Setup

```powershell
cd "C:\Users\TONY\Downloads\UpSkill-project\Grocery Store"
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

