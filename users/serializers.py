from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

class UserBaseValidation(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserAuthSerializer(UserBaseValidation):
    pass

class UserCreateSerializer(UserBaseValidation):
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User already exists!')
        return username
    
class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6, min_length=6)