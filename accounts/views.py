# functionner, HTTP response, url
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)



