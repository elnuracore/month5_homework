import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserConfirmation
from .serializers import (
    UserAuthSerializer, 
    UserCreateSerializer, 
    UserConfirmationSerializer
)

class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"key": token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = str(random.randint(100000, 999999))
        UserConfirmation.objects.create(user=user, code=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'code': code}
        )

class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']

        try:
            confirmation = UserConfirmation.objects.get(user__username=username, code=code)
        except UserConfirmation.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND, 
                data={'error': 'Invalid code or username'}
            )
            
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'User activated successfully'})