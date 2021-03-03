from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('search', csrf_exempt(views.search_expenses), name='search'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    path('expense-summary', views.expense_summary, name='expense-summary'),
    path('view-expense-summary', views.view_expense_summary, name='view-expense-summary'),
    path('monthly-expenses', views.get_monthly_expense_summary, name='monthly-expenses')
]
