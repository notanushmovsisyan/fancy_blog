# converting data types, forms
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist


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
        user.password = serializers.validate_password()
        user.set_password(validated_data['password'])
        user.save()
        return user


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyTokenAndChangePasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        try:
            u = CustomUser.objects.get(id=data['user_id'])
            validate_password(data['newPassword'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"message": "This user does not exist."})
        return data

