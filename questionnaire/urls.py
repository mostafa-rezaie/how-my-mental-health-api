from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Questionnaire.as_view(), name='questionnaire'),
    path('all-questionnaire', views.AllQuestionnaires.as_view(), name='all_questionnaire'),

]
