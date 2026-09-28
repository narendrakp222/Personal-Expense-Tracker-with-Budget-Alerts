from django.urls import path
from . import views

urlpatterns = [
    path("category/", views.category_list, name="category_list"),
    path("category/create/", views.category_create, name="category_create"),
    path("category/update/<int:id>/", views.category_update, name="category_update"),
    path("category/delete/<int:id>/", views.category_delete, name="category_delete"),
]