from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/update/<int:id>/", views.category_update, name="category_update"),
    path("categories/delete/<int:id>/", views.category_delete, name="category_delete"),
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/create/", views.budget_create, name="budget_create"),
    path("budgets/update/<int:id>/", views.budget_update, name="budget_update"),
    path("budgets/delete/<int:id>/", views.budget_delete, name="budget_delete"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/create/", views.expense_create, name="expense_create"),
    path("expenses/update/<int:id>/", views.expense_update, name="expense_update"),
    path("expenses/delete/<int:id>/", views.expense_delete, name="expense_delete"),
]
