from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', csrf_exempt(views.search_income), name='search'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income, name='delete-income')
]