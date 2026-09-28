from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BudgetForm, CategoryForm, ExpenseForm, RegisterForm
from .models import Budget, Category, Expense, monthly_spent_for_category


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Logged in successfully.")
        return redirect("dashboard")
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def _alert_level(utilization):
    if utilization >= 100:
        return "danger"
    if utilization >= 80:
        return "warning"
    return "success"


@login_required
def dashboard(request):
    current = date.today().replace(day=1)

    budgets = Budget.objects.filter(
        user=request.user,
        month_year__year=current.year,
        month_year__month=current.month
    ).select_related("category")

    category_rows = []

    total_budget = 0
    total_spent = 0

    for budget in budgets:

        spent = monthly_spent_for_category(
            request.user,
            budget.category,
            budget.month_year
        )

        utilization = (
            float(spent / budget.monthly_limit * 100)
            if budget.monthly_limit
            else 0
        )

        total_budget += budget.monthly_limit
        total_spent += spent

        category_rows.append({
            "budget": budget,
            "spent": spent,
            "remaining": budget.monthly_limit - spent,
            "utilization": utilization,
            "alert": _alert_level(utilization),
        })

    monthly_summary = (
        Expense.objects.filter(
            user=request.user,
            date__year=current.year,
            date__month=current.month
        )
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    # -----------------------------
    # Chart Data
    # -----------------------------
    chart_labels = []
    chart_totals = []

    for item in monthly_summary:
        chart_labels.append(item["category__name"])
        chart_totals.append(float(item["total"]))

    recent_expenses = (
        Expense.objects
        .filter(user=request.user)
        .select_related("category")
        .order_by("-date")[:10]
    )

    context = {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": total_budget - total_spent,
        "category_rows": category_rows,
        "monthly_summary": monthly_summary,
        "recent_expenses": recent_expenses,

        # Chart.js
        "chart_labels": chart_labels,
        "chart_totals": chart_totals,
    }

    return render(
        request,
        "dashboard.html",
        context
    )
@login_required
def category_list(request):
    return render(request, "category/category_list.html", {"categories": Category.objects.filter(user=request.user)})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, "Category created.")
        return redirect("category_list")
    return render(request, "category/category_create.html", {"form": form})


@login_required
def category_update(request, id):
    obj = get_object_or_404(Category, id=id, user=request.user)
    form = CategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated.")
        return redirect("category_list")
    return render(request, "category/category_update.html", {"form": form, "category": obj})


@login_required
def category_delete(request, id):
    obj = get_object_or_404(Category, id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Category deleted.")
        return redirect("category_list")
    return render(request, "category/category_delete.html", {"category": obj})


@login_required
def budget_list(request):
    return render(request, "budget/budget_list.html", {"budgets": Budget.objects.filter(user=request.user).select_related("category")})


@login_required
def budget_create(request):
    form = BudgetForm(request.POST or None)
    form.fields["category"].queryset = Category.objects.filter(user=request.user)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, "Budget created.")
        return redirect("budget_list")
    return render(request, "budget/budget_create.html", {"form": form})


@login_required
def budget_update(request, id):
    obj = get_object_or_404(Budget, id=id, user=request.user)
    form = BudgetForm(request.POST or None, instance=obj)
    form.fields["category"].queryset = Category.objects.filter(user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Budget updated.")
        return redirect("budget_list")
    return render(request, "budget/budget_create.html", {"form": form, "budget": obj})


@login_required
def budget_delete(request, id):
    obj = get_object_or_404(Budget, id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Budget deleted.")
        return redirect("budget_list")
    return render(request, "budget/budget_delete.html", {"budget": obj})


@login_required
def expense_list(request):
    return render(request, "expense/expense_list.html", {"expenses": Expense.objects.filter(user=request.user).select_related("category")})


@login_required
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    form.fields["category"].queryset = Category.objects.filter(user=request.user)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, "Expense saved.")
        return redirect("expense_list")
    return render(request, "expense/expense_create.html", {"form": form})


@login_required
def expense_update(request, id):
    obj = get_object_or_404(Expense, id=id, user=request.user)
    form = ExpenseForm(request.POST or None, instance=obj)
    form.fields["category"].queryset = Category.objects.filter(user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Expense updated.")
        return redirect("expense_list")
    return render(request, "expense/expense_update.html", {"form": form, "expense": obj})


@login_required
def expense_delete(request, id):
    obj = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Expense deleted.")
        return redirect("expense_list")
    return render(request, "expense/expense_delete.html", {"expense": obj})
