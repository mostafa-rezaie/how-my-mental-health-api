from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from knox.auth import TokenAuthentication

from profile_api.serializers import UserProfileSerializer
from profile_api.models import UserProfile
from profile_api.serializers import UserProfileSerializer, LoginSerializer


# Create your views here.


class RegisterNewUser(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = serializer.data.copy()
        data['message'] = 'user successfully registered'
        data['token'] = AuthToken.objects.create(user)[1]
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class AuthenticateUser(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = TokenAuthentication
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # serializer = LoginSerializer(data=request.data, context={'request': self.request})
        # serializer.is_valid(raise_exception=True)
        email = request.data['email']
        password = request.data['password']
        try:
            user = UserProfile.objects.get(email=email)
        except:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.check_password(password):
            login(request, user=user)
            # print('success')
        else:
            return Response({'message': 'incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            # print('incorrect password')
        token = AuthToken.objects.create(user=user)[1]
        return Response({'message': 'login successful', 'token': token}, status=status.HTTP_202_ACCEPTED)


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'})


class Test(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'allowed'})
