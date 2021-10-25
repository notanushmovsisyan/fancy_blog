from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import accounts.views as views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('reset-password-email/', views.ResetPasswordEmailView.as_view(), name='reset_password_email'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile-picture-upload/', views.ProfilePictureUploadView.as_view(), name='profile-picture-upload'),
]
