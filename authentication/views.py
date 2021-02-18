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
    # get user data
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    context = {
      'username': username,
      'email': email
    }

    # validate data
    if not User.objects.filter(username=username).exists():
      if not User.objects.filter(email=email).exists():
        if len(password) < 6:
          messages.error(request, 'Password too short')
          return render(request, 'authentication/register.html', context)

        # register user
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully")
        return render(request, 'authentication/register.html')

    return render(request, 'authentication/register.html')