from .models import Question, Questionnaires,Answers
from rest_framework.generics import ListAPIView,CreateAPIView
from .serializers import QuestionSerializer, QuestionnaireSerializer
from django.http import HttpResponse, JsonResponse


class Questionnaire(ListAPIView):
    queryset = Question.objects.all().filter(questionnaire__name__exact='s1')
    serializer_class = QuestionSerializer


class AllQuestionnaires(ListAPIView):
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnaireSerializer


class Questions(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        qname = self.kwargs['qname']
        questionnaire = Questionnaires.objects.get(name__icontains=qname)
        qs2 = Question.objects.filter(questionnaire=questionnaire)
        return qs2

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except:
            return JsonResponse({'message': 'questionnaire Not Found'},status=404)


class Answer(CreateAPIView):
    def post(self, request, *args, **kwargs):
        print(request.data['data'])
        answers = request.data['data']
        user = request.user
        question = Question.objects.get(qid=1)
        answer = Answer(user = user , )
        for answer in answers:
            
        return HttpResponse('hh')
