from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.urls import reverse
from django.contrib import auth
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator


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
        user.is_active = False
        user.save()

        # sending mail to user for account activation
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('authentication:activate-account', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
        activate_url = f"http://{domain}{link}"
        email = EmailMessage(
          'Activate You Account',
          'You have succeesfully created your account. You need to activate your account before using it. Please use the below link to activate the account:\n ' + activate_url,
          'admin@admin.com',
          [email],
        )
        email.send(fail_silently=False)
        messages.success(request, "Account created successfully")
        return render(request, 'authentication/register.html')

    return render(request, 'authentication/register.html')


class VerificationView(View):
  def get(self, request, uidb64, token):
    try:
      id = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=id)

      if not token_generator.check_token(user, token):
        return redirect('authentication:login' + '?message=' + 'User already activated')

      if user.is_active:
        return redirect('authentication:login')

      user.is_active = True
      user.save()
      messages.success(request, 'Account activated successfully.')
      return redirect('authentication:login')

    except Exception as e:
      pass

    return redirect('authentication:login')


class LoginView(View):
  def get(self, request):
    return render(request, 'authentication/login.html')

  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']

    if username and password:
      user = auth.authenticate(username=username, password=password)

      if user:

        if user.is_active:
          auth.login(request, user)
          return redirect('/expenses')

        messages.error(request, 'Account not active. Please check your mail to activate your account.')
        return render(request, 'authentication/login.html')

      messages.error(request, 'Invalid credentials. Please check your username/password.')
      return render(request, 'authentication/login.html')

    messages.error(request, 'Please enter your username/password.')
    return render(request, 'authentication/login.html')


class LogoutView(View):
  def get(self, request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged out.')
    return redirect('authentication:login')


class PasswordResetRequest(View):
  def get(self, request):
    return render(request, 'authentication/reset-password.html')

  def post(self, request):
    email = request.POST['email']
    context = {
      'values': email 
    }

    # Validate email
    if not validate_email(email):
      messages.error(request, 'Email address is not valid.')
      return render(request, 'authentication/reset-password.html', context)

    # check user
    user = User.objects.filter(email=email)
    if not user.exists():
      messages.error(request, 'Account does not exists.')
      return render(request, 'authentication/reset-password.html', context)

    # Send reset link to user
    uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
    domain = get_current_site(request).domain
    link = reverse('authentication:reset-user-password', kwargs={'uidb64': uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})
    reset_url = f"http://{domain}{link}"
    email = EmailMessage(
      'Reset Your Password',
      'Please use the below link to reset your account password:\n ' + reset_url,
      'admin@admin.com',
      [email],
    )
    email.send(fail_silently=False)
    messages.success(request, 'Password reset link sent.')
    return render(request, 'authentication/reset-password.html')


class PasswordResetView(View):
  def get(self, request, uidb64, token):
    context = {
      'uidb64': uidb64,
      'token': token
    }

    user_id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=user_id)
    if not PasswordResetTokenGenerator().check_token(user, token):
      messages.info(request, 'Password reset link is invalid. Please request a new one.')
      return render(request, 'authentication/reset-password.html')

    return render(request, 'authentication/set-newpassword.html', context)

  def post(self, request, uidb64, token):
    context = {
      'uidb64': uidb64,
      'token': token
    }

    password = request.POST['password']
    password2 = request.POST['password2']

    if password != password2:
      messages.error(request, 'Passwords do not match.')
      return render(request, 'authentication/set-newpassword.html', context)

    if len(password) < 6:
      messages.error(request, 'Password is too short. Please choose password with atleast 6 characters.')
      return render(request, 'authentication/set-newpassword.html', context)

    user_id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=user_id)
    user.set_password(password)
    user.save()

    messages.success(request, 'Password reset successful.')
    return render(request, 'authentication/reset-successful.html')
