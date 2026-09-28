# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# from .models import Budget


# @login_required
# def budget_list(request):
#     budgets = (
#         Budget.objects.filter(user=request.user)
#         .select_related("category")
#         .order_by("-month_year")
#     )
#     return render(request, "budget/budget_list.html", {"budgets": budgets})




from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BudgetForm
from .models import Budget


@login_required
def budget_list(request):
    budgets = (
        Budget.objects.filter(user=request.user)
        .select_related("category")
        .order_by("-month_year")
    )
    return render(request, "budget/budget_list.html", {"budgets": budgets})


@login_required
def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("budget_list")
    else:
        form = BudgetForm(user=request.user)

    return render(request, "budget/budget_create.html", {"form": form})