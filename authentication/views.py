from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages


class UsernameValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    username = data['username']

    # check if username is a valid string
    if not str(username).isalnum():
      return JsonResponse({'username_error': 'Username is not valid.'}, status=400)
    # check if username already exists in db
    if User.objects.filter(username=username).exists():
      return JsonResponse({'username_error': 'Username already exists.'}, status=409)

    return JsonResponse({'username_valid': True}, status=200)


class EmailValidationView(View):
  def post(self, request):
    data = json.loads(request.body)
    email = data['email']

    # check if email is valid
    if not validate_email(email):
      return JsonResponse({'email_error': 'Email is not valid.'}, status=400)
    # check if email already exists in db
    if User.objects.filter(email=email).exists():
      return JsonResponse({'email_error': 'Email address already exists.'}, status=409)

    return JsonResponse({'email_valid': True})


class RegistrationView(View):
  def get(self, request):
    return render(request, 'authentication/register.html')

  def post(self, request):
    messages.success(request, 'Success Message')
    messages.error(request, 'Error Message')
    messages.info(request, 'Info Message')
    messages.warning(request, 'Warning Message')
    return render(request, 'authentication/register.html')