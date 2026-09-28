from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Budget, Category, Expense

admin.site.site_header = "Expense Tracker Admin"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "description")
    list_filter = ("user",)
    search_fields = ("name", "user__username")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "user", "monthly_limit", "month_year")
    list_filter = ("user", "month_year")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "category", "user", "date", "notes")
    list_filter = ("user", "date", "category")
    search_fields = ("notes",)
