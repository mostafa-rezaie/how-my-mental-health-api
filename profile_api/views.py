from django.shortcuts import render
from profile_api.serializers import UserProfileSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from profile_api.models import UserProfile
from profile_api.serializers import UserProfileSerializer
from django.http import HttpResponse
# Create your views here.


class RegisterNewUser(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
