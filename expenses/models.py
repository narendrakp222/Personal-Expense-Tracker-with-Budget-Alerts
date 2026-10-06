from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month_year = models.DateField()

    class Meta:
        unique_together = ("user", "category", "month_year")
        ordering = ["-month_year", "category__name"]

    def clean(self):
        if self.monthly_limit is not None and self.monthly_limit <= 0:
            raise ValidationError({"monthly_limit": "Monthly limit must be greater than zero."})
        if self.category_id and self.user_id and self.category.user_id != self.user_id:
            raise ValidationError({"category": "Category must belong to the same user."})

    def __str__(self):
        return f"{self.category} - {self.month_year:%Y-%m}"


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def clean(self):
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({"amount": "Amount must be greater than zero."})
        if self.category_id and self.user_id and self.category.user_id != self.user_id:
            raise ValidationError({"category": "Category must belong to the same user."})

    def __str__(self):
        return f"{self.amount} on {self.date}"


def monthly_spent_for_category(user, category, month_year):
    return (
        Expense.objects.filter(
            user=user,
            category=category,
            date__year=month_year.year,
            date__month=month_year.month,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    )


def budget_alert_level(utilization):
    if utilization >= 100:
        return "danger"
    if utilization >= 80:
        return "warning"
    return "success"


def budget_utilization(spent, monthly_limit):
    if not monthly_limit:
        return Decimal("0")
    return spent / monthly_limit * Decimal("100")
