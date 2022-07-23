from django.shortcuts import render
from profile_api.serializers import UserProfileSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from profile_api.models import UserProfile
from profile_api.serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from knox.models import AuthToken
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
