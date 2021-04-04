from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', csrf_exempt(views.search_income), name='search'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income, name='delete-income'),
    path('view-income-summary', views.view_income_summary, name='view-income-summary'),
    path('income-summary', views.income_summary, name='income-summary'),
    path('monthly-income', views.get_monthly_income_summary, name='monthly-income'),
    path('export-pdf', views.export_pdf, name='export-pdf')
]