from django.contrib import admin
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-expense', views.add_expense, name='add-expense')
]
