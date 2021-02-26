from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-income', views.add_income, name='add-income')
]