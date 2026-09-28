from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from expenses.models import Budget, Category, Expense


class Command(BaseCommand):
    help = "Seed demo data for the expense tracker"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="demouser", defaults={"email": "demo@example.com"})
        user.set_password("demo12345")
        user.save()

        food, _ = Category.objects.get_or_create(user=user, name="Food", defaults={"description": "Groceries and dining"})
        travel, _ = Category.objects.get_or_create(user=user, name="Travel", defaults={"description": "Transport costs"})

        Budget.objects.get_or_create(user=user, category=food, month_year=date.today().replace(day=1), defaults={"monthly_limit": 5000})
        Budget.objects.get_or_create(user=user, category=travel, month_year=date.today().replace(day=1), defaults={"monthly_limit": 3000})

        Expense.objects.get_or_create(user=user, category=food, date=date.today(), defaults={"amount": 750, "notes": "Lunch and groceries"})
        Expense.objects.get_or_create(user=user, category=travel, date=date.today(), defaults={"amount": 120, "notes": "Auto fare"})

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
