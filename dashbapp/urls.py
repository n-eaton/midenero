
from django.urls import path


from . import views

urlpatterns = [
    path("base", views.base, name="base"),
    path("", views.expenses, name="expenses"),
    path("add_expense", views.add_expense, name="add_expense"),
  
]
