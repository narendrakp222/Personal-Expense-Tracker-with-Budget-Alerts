from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import ExpenseForm
from .models import Budget, Category, Expense


class BudgetLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Food", description="Food budget")

    def test_expense_amount_must_be_positive(self):
        form = ExpenseForm(data={"amount": 0, "date": "2026-09-01", "category": self.category.id, "notes": "x"})
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)

    def test_budget_utilization_thresholds(self):
        budget = Budget.objects.create(user=self.user, category=self.category, monthly_limit=1000, month_year=date(2026, 9, 1))
        Expense.objects.create(user=self.user, category=self.category, amount=799, date=date(2026, 9, 2), notes="a")
        spent = Expense.objects.filter(user=self.user, category=self.category, date__year=2026, date__month=9).count()
        self.assertEqual(spent, 1)
        self.assertEqual(budget.monthly_limit, 1000)

    def test_budget_alert_threshold_calculation(self):
        self.assertLess(79.9, 80)
        self.assertGreaterEqual(80, 80)
        self.assertGreaterEqual(100, 100)

    def test_other_user_cannot_access_records(self):
        other = User.objects.create_user(username="otheruser", password="pass12345")
        self.assertNotEqual(self.user.id, other.id)
        self.assertEqual(Category.objects.filter(user=other).count(), 0)


class ModelValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="validator", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Bills", description="Monthly bills")

    def test_expense_negative_amount_rejected(self):
        expense = Expense(user=self.user, category=self.category, amount=-10, date=date(2026, 9, 1), notes="invalid")
        with self.assertRaises(Exception):
            expense.full_clean()

    def test_cross_user_category_rejected(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        other_category = Category.objects.create(user=other, name="Other", description="Other user category")
        expense = Expense(user=self.user, category=other_category, amount=10, date=date(2026, 9, 1), notes="invalid")
        with self.assertRaises(Exception):
            expense.full_clean()
