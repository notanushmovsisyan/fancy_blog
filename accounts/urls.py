# vieweri hamar
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    # path('', include('django_registration.backends.activation.urls')),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', )

]