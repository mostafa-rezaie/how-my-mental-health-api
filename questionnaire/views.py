from .models import Question, Questionnaires, Answers, Results
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import QuestionSerializer, QuestionnaireSerializer
from django.http import HttpResponse, JsonResponse
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json


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
            return JsonResponse({'message': 'questionnaire Not Found'}, status=404)


class Answer(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # serializer_class = AnswerSerializer

    def post(self, request, *args, **kwargs):
        # print(request.data['data'])
        answers = request.data['data']
        user = request.user
        questionnaire_id = request.data['questionnaireId']
        try:
            questionnaire = Questionnaires.objects.get(id=questionnaire_id)
        except:
            return Response({'message': 'this questionnaire does not exist'})
        questionnaire_name = questionnaire.name
        # print(request.user)
        question_counter = 0
        for answer in answers:
            question_counter = question_counter + 1
            qid = answer['qid']
            answer_choice = answer['answer']
            question = Question.objects.filter(questionnaire__name__contains=questionnaire_name).get(
                qid__contains=qid)
            Answers.objects.create(user=request.user, question=question, answer=answer_choice)
        score = question_counter * 3.1
        Results.objects.create(user=request.user, num_of_question_answered=question_counter, duration=320, score=score)
        return Response({'message': 'answers submitted successfully'})
