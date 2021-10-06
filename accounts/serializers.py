# converting data types
# stex em password validation anum? Karam anem?
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # WHA
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = CustomUser
        fields = ('user_id', 'email', 'first_name', 'last_name',
                  'phone_number', 'password', 'profile_picture'),
        extra_kwargs = {'password': {'write_only': True}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email # Emailov anem? Hn?
        return token

