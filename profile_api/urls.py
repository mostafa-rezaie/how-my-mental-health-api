from django.urls import path
from . import views
from knox.views import LogoutView

urlpatterns = [
    path('sign-up', views.RegisterNewUser.as_view()),
    path('login', views.AuthenticateUser.as_view()),
    path('logout', LogoutView.as_view()),
]
