from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import BudgetForm, ExpenseForm
from .models import (
    Budget,
    Category,
    Expense,
    budget_alert_level,
    budget_utilization,
    monthly_spent_for_category,
)


class BudgetCalculationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Food", description="Food budget")
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            monthly_limit=Decimal("1000.00"),
            month_year=date(2026, 9, 1),
        )

    def test_monthly_spent_uses_user_category_and_month(self):
        other = User.objects.create_user(username="otheruser", password="pass12345")
        other_category = Category.objects.create(user=other, name="Food", description="")

        Expense.objects.create(user=self.user, category=self.category, amount=Decimal("450.50"), date=date(2026, 9, 2))
        Expense.objects.create(user=self.user, category=self.category, amount=Decimal("349.50"), date=date(2026, 9, 20))
        Expense.objects.create(user=self.user, category=self.category, amount=Decimal("50.00"), date=date(2026, 10, 1))
        Expense.objects.create(user=other, category=other_category, amount=Decimal("999.00"), date=date(2026, 9, 3))

        spent = monthly_spent_for_category(self.user, self.category, self.budget.month_year)

        self.assertEqual(spent, Decimal("800"))
        self.assertEqual(budget_utilization(spent, self.budget.monthly_limit), Decimal("80.0"))

    def test_budget_alert_thresholds(self):
        self.assertEqual(budget_alert_level(Decimal("79.99")), "success")
        self.assertEqual(budget_alert_level(Decimal("80.00")), "warning")
        self.assertEqual(budget_alert_level(Decimal("99.99")), "warning")
        self.assertEqual(budget_alert_level(Decimal("100.00")), "danger")


class FormValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="forms", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Bills", description="Monthly bills")

    def test_expense_amount_must_be_positive(self):
        form = ExpenseForm(
            data={"amount": 0, "date": "2026-09-01", "category": self.category.id, "notes": "x"},
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)

    def test_budget_month_input_is_normalized(self):
        form = BudgetForm(
            data={"category": self.category.id, "monthly_limit": "1500.00", "month_year": "2026-09"},
            user=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["month_year"], date(2026, 9, 1))

    def test_cross_user_category_rejected_by_model_validation(self):
        other = User.objects.create_user(username="other2", password="pass12345")
        other_category = Category.objects.create(user=other, name="Other", description="Other user category")
        expense = Expense(user=self.user, category=other_category, amount=10, date=date(2026, 9, 1), notes="invalid")

        with self.assertRaises(Exception):
            expense.full_clean()


class ExpenseCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="spender", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Food", description="")
        self.client.force_login(self.user)

    def test_create_expense_accepts_category_name_and_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("expense_create"),
            {"amount": "45.50", "date": "2026-09-15", "category": "Food", "notes": "Lunch with client"},
        )

        self.assertRedirects(response, reverse("dashboard"))
        expense = Expense.objects.get(user=self.user)
        self.assertEqual(expense.amount, Decimal("45.50"))
        self.assertEqual(expense.category, self.category)

    def test_create_expense_rejects_other_users_category(self):
        other = User.objects.create_user(username="other3", password="pass12345")
        Category.objects.create(user=other, name="Travel", description="")

        response = self.client.post(
            reverse("expense_create"),
            {"amount": "45.50", "date": "2026-09-15", "category": "Travel", "notes": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Expense.objects.filter(user=self.user).exists())


class AccessAndDeletionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="pass12345")
        self.category = Category.objects.create(user=self.user, name="Utilities", description="")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_login_page_renders_for_anonymous_user(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_update_another_users_category(self):
        other = User.objects.create_user(username="other4", password="pass12345")
        other_category = Category.objects.create(user=other, name="Hidden", description="")
        self.client.force_login(self.user)

        response = self.client.get(reverse("category_update", args=[other_category.id]))

        self.assertEqual(response.status_code, 404)

    def test_category_with_expenses_is_not_deleted(self):
        Expense.objects.create(user=self.user, category=self.category, amount=Decimal("20.00"), date=date(2026, 9, 1))
        self.client.force_login(self.user)

        response = self.client.post(reverse("category_delete", args=[self.category.id]))

        self.assertRedirects(response, reverse("category_list"))
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())
