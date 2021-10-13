# functionner, HTTP response, url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegistrationSerializer, ResetPasswordEmailSerializer, VerifyTokenAndChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail.backends.smtp import EmailBackend
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from accounts.mail_service import send_mail


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Registration was successfully completed."})


class ResetPasswordEmail(generics.CreateAPIView):
    serializer_class = ResetPasswordEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response({"message": "Password reset email sent."})

        if not CustomUser.objects.filter(email=serializer.data['email']).exists():
            return response

        user = CustomUser.objects.get(email=serializer.data['email'])
        token = default_token_generator.make_token(user=user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        send_mail(self, token, uidb64, serializer.data['email'])

        return response


class VerifyTokenAndChangePassword(generics.CreateAPIView):
    serializer_class = VerifyTokenAndChangePasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(id=serializer.data['user_id'])
        user.set_password(serializer.data['newPassword'])
        response = "Password has been successfully."

        return Response({"message": response})
