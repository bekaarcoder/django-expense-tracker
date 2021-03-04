from django.urls import path
from .views import (
    RegistrationView,
    UsernameValidationView,
    EmailValidationView,
    VerificationView,
    LoginView,
    LogoutView,
    PasswordResetRequest,
    PasswordResetView
)
from django.views.decorators.csrf import csrf_exempt

app_name = "authentication"

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path(
        "validate-username",
        csrf_exempt(UsernameValidationView.as_view()),
        name="validate-username",
    ),
    path(
        "validate-email",
        csrf_exempt(EmailValidationView.as_view()),
        name="validate-email",
    ),
    path(
        "activate-account/<uidb64>/<token>",
        VerificationView.as_view(),
        name="activate-account",
    ),
    path(
        "reset-password-request",
        PasswordResetRequest.as_view(),
        name="reset-password-request",
    ),
    path(
      'reset-user-password/<uidb64>/<token>',
      PasswordResetView.as_view(),
      name='reset-user-password'
    )
]