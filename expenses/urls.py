from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>',views.edit_expense, name='edit-expense')
]
