
from django.urls import path
 
from . import views
 
urlpatterns = [
    path("budget/", views.budget_list, name="budget_list"),
    path("budget/create/", views.budget_create, name="budget_create"),
    path("budget/update/<int:id>/", views.budget_update, name="budget_update"),
    path("budget/delete/<int:id>/", views.budget_delete, name="budget_delete"),
]
