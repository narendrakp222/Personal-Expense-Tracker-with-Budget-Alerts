from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Budget


@login_required
def budget_list(request):
    budgets = (
        Budget.objects.filter(user=request.user)
        .select_related("category")
        .order_by("-month_year")
    )
    return render(request, "budget/budget_list.html", {"budgets": budgets})