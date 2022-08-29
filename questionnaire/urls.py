from django.urls import path, include
from . import views

urlpatterns = [
    path('all-questionnaire', views.AllQuestionnaires.as_view(), name='all_questionnaire'),
    path('get-questions/<str:qname>', views.Questions.as_view(), name='all_questions'),
    path('submit-answers', views.Answer.as_view(), name='submit_answers'),
    path('', views.Questionnaire.as_view(), name='questionnaire'),

]
