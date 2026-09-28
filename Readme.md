# Personal Expense Tracker with Budget Alerts

Full-stack Django application for tracking categories, budgets, and expenses with budget alerts.

## Features
- Register, login, logout
- Protected user-specific CRUD for categories, budgets, and expenses
- Dashboard with totals, category spending, monthly summary, and alert badges
- Bootstrap 5 responsive UI
- Validation for positive expense amounts
- Demo seed command

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Run server: `python manage.py runserver`

## Tests
Run:
`python manage.py test`



## Demo Data
Seed demo data:
`python manage.py seed_demo_data`

