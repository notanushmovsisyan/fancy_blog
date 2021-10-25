from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )
        user.password = validate_password()
        user.set_password(validated_data['password'])
        user.save()
        return user


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    user_id = serializers.CharField()
    token = serializers.CharField()

    def validate_user_id(self, user_id):
        user_id = urlsafe_base64_decode(user_id)
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise ValidationError("This user does not exist.")
        finally:
            if not CustomUser.objects.filter(id=user_id).exists:
                raise ValidationError("This user does not exist.")
        return user_id

    def validate_new_password(self, new_password):
        try:
            validate_password(new_password)
        except ValidationError:
            raise ValidationError("This password is invalid.")
        return new_password

    def validate(self, data):  # TODO: doesn't validate
        try:
            default_token_generator.check_token(data['user_id'], data['token'])
        except ValueError:
            raise ValidationError("This user does not have permission to reset password.")
        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'password2', 'old_password')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not self.context['user'].check_password(data['old_password']):
            raise ValidationError({"old_password": "Old password is not correct"})
        return data


class ProfilePictureUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    phone_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('image', 'email', 'first_name', 'last_name', 'phone_number')
        read_only_fields = ('email', 'first_name', 'last_name', 'phone_number')
