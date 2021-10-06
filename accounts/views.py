#functionner, HTTP response, url
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegistrationSerializer, CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
