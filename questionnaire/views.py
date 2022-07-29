from .models import Question, Questionnaires
from rest_framework.generics import ListAPIView
from .serializers import QuestionSerializer, QuestionnaireSerializer
from django.http import HttpResponse


class Questionnaire(ListAPIView):
    queryset = Question.objects.all().filter(questionnaire__name__exact='s1')
    serializer_class = QuestionSerializer


class AllQuestionnaires(ListAPIView):
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnaireSerializer


class Questions(ListAPIView):
    def get(self, request, *args, **kwargs):
        print(kwargs['qname'])
        qs = Questionnaires.objects.all()
        qs1 = Questionnaires.objects.values_list('name',flat=True)
        print(list(qs1))
        return HttpResponse('hey')
