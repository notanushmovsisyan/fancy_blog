from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import RegistrationView, ResetPasswordEmailView, ResetPasswordView, ChangePasswordView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'), #TODO: TokenObtainPairSerializer
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('reset-password-email/', ResetPasswordEmailView.as_view(), name='reset_password_email'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
