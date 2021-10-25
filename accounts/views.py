from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from accounts.mail_service import send_mail


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user


class ResetPasswordEmailView(generics.CreateAPIView):
    serializer_class = serializers.ResetPasswordEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response({"message": "Password reset email sent."})

        if not CustomUser.objects.filter(email=serializer.data['email']).exists():
            return response

        user = CustomUser.objects.get(email=serializer.data['email'])
        token = default_token_generator.make_token(user=user.id)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        send_mail(token, uidb64, serializer.data['email'])
        return response


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(id=serializer.data['user_id'])
        user.set_password(serializer.data['new_password'])
        response = "Password has been set successfully."

        return Response({"message": response})


class ChangePasswordView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.data['password'])
        request.user.save()
        return Response({"message": "Password has been set successfully."})


class ProfilePictureUploadView(generics.CreateAPIView):
    serializer_class = serializers.ProfilePictureUploadSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
