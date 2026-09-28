# Personal Expense Tracker with Budget Alerts

A modern Django-based Personal Expense Tracker that helps users manage daily expenses, set monthly budgets, and receive visual alerts when spending approaches or exceeds predefined limits.

## Features

### User Authentication

* User Registration
* User Login
* User Logout
* Secure user-specific data isolation

### Category Management

* Create Categories
* View Categories
* Update Categories
* Delete Categories

### Budget Management

* Set Monthly Budget Limits
* Update Budget Limits
* Category-wise Budget Tracking
* Monthly Budget Records

### Expense Management

* Add Expenses
* Edit Expenses
* Delete Expenses
* Expense History Tracking
* Optional Notes Support

### Dashboard Analytics

* Total Monthly Spending
* Total Monthly Budget
* Remaining Budget
* Category-wise Spending Summary
* Recent Expense Activity
* Budget Utilization Tracking
* Chart.js Analytics Dashboard

### Budget Alert System

* Safe Status (< 80%)
* Warning Status (≥ 80%)
* Danger Status (≥ 100%)

## Technology Stack

### Backend

* Django
* SQLite

### Frontend

* Django Templates
* Bootstrap 5
* Bootstrap Icons
* Custom CSS
* Chart.js

### Database

* SQLite

## Project Structure

```text
expense_tracker/
│
├── expense_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── expenses/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── templates/
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── category/
│   ├── budget/
│   ├── expense/
│   ├── base.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd expense_tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000/
```

## Security Features

* Login Required for Protected Pages
* User-specific Data Access
* Secure CRUD Operations
* Category Isolation
* Budget Isolation
* Expense Isolation

## Validation Rules

### Expense Validation

* Amount must be greater than zero
* Negative values are rejected
* Zero values are rejected

### Authorization Rules

* Users can only access their own data
* Unauthorized records return 404
* Protected routes require authentication

## Testing

Run tests using:

```bash
python manage.py test
```

## Future Enhancements

* Export Expenses to CSV
* PDF Reports
* Dark Mode
* Monthly Email Reports
* AI Spending Insights
* Recurring Expenses
* Advanced Charts

## Developed For

SVCET Hackathon – Powered by LEARNSQUARE

### Theme

Personal Expense Tracker with Budget Alerts

### Team

🦏 Rangers
