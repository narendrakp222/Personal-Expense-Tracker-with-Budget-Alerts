

# Personal Expense Tracker with Budget Alerts

A Django-based web application for managing personal expenses, budgets, and spending.

## Features

* User authentication
* Category management
* Expense management
* Monthly budgets
* Category-wise budgets
* Budget alerts
* Spending dashboard
* Expense history
* Chart.js analytics

## Budget Alerts

* **Safe:** Below 80%
* **Warning:** 80%–99%
* **Danger:** 100% or above

## Tech Stack

* Python
* Django
* SQLite
* Bootstrap 5
* JavaScript
* Chart.js

## Architecture

```text
                User
                 |
                 v
        +------------------+
        |  Django Templates |
        |   Bootstrap / JS  |
        +--------+---------+
                 |
                 v
        +------------------+
        |   Django Views   |
        +--------+---------+
                 |
        +--------+---------+
        |                  |
        v                  v
   Forms / Auth        Business Logic
        |                  |
        +--------+---------+
                 |
                 v
        +------------------+
        |    Django ORM    |
        +--------+---------+
                 |
                 v
        +------------------+
        |      SQLite      |
        +------------------+
```

## Project Structure

```text
expense_tracker/
├── expense_tracker/
│   ├── settings.py
│   └── urls.py
│
├── expenses/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/narendrakp222/Personal-Expense-Tracker-with-Budget-Alerts.git
cd Personal-Expense-Tracker-with-Budget-Alerts

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Testing

```bash
python manage.py test
```

## Hackathon

**SVCET Hackathon — Powered by LEARNSQUARE**

