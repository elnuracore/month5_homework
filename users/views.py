from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import UserConfirmation
import random
from rest_framework.decorators import api_view
from .serializers import UserAuthSerializer, UserCreateSerializer, UserConfirmationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


# @api_view(['POST'])
# def authorization_api_view(request):
class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"key" : token.key})

        return Response(status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST'])
# def registration_api_view(request):
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = str(random.randint(100000, 999999))
        UserConfirmation.objects.create(user=user, code=code)
        return Response(status=status.HTTP_201_CREATED,

        data={'user_id': user.id, 'code': code})


# @api_view(["POST"])
# def confirm_api_view(request):
class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            confirmation = UserConfirmation.objects.get(user__username=username, code=code)
        except UserConfirmation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                data={'error': 'Invalid code or username'})

        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'User activated successfully'})




