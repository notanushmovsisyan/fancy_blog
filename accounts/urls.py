# vieweri hamar
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import RegistrationView, ResetPasswordEmail, VerifyTokenAndChangePassword

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('reset-password-email/', ResetPasswordEmail.as_view(), name='reset_password_email'),
    path('change-password/', VerifyTokenAndChangePassword.as_view(), name='change-password'),
]