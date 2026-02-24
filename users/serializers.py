from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'is_superuser']

    def validate(self, data):
        is_superuser = data.get('is_superuser', self.instance.is_superuser if self.instance else False)
        phone = data.get('phone_number')

        if is_superuser and not phone:
            raise serializers.ValidationError(
                {"phone_number": "Суперпользователь должен иметь номер телефона."}
            )
        return data

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