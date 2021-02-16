from django.urls import path
from .views import RegistrationView

app_name = 'authentication'

urlpatterns = [
  path('register', RegistrationView.as_view(), name='register')
]