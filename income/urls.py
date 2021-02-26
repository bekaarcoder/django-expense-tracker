from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income, name='delete-income')
]