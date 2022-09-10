from .models import Question, Questionnaires, Answers, Results
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import QuestionSerializer, QuestionnaireSerializer, ResultsSerializer
from django.http import HttpResponse, JsonResponse
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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
        answers = request.data['data']
        user = request.user
        questionnaire_id = request.data['questionnaireId']
        try:
            questionnaire = Questionnaires.objects.get(id=questionnaire_id)
        except:
            return Response({'message': 'this questionnaire does not exist'})
        questionnaire_name = questionnaire.name
        question_count = Question.objects.filter(questionnaire__name=questionnaire_name).count()
        answers_count = len(answers)
        if answers_count != question_count:
            return Response({'message': 'questionnaire is not answered completely'}, status=status.HTTP_400_BAD_REQUEST)
        print('>>>>>>>>>>>', len(answers))
        sum_ans = 0
        for answer in answers:
            qid = answer['qid']
            answer_choice = answer['answer']
            sum_ans = sum_ans + int(answer_choice)
            question = Question.objects.filter(questionnaire__name=questionnaire_name).get(
                qid=qid)
            Answers.objects.create(user=request.user, question=question, answer=answer_choice)
        if questionnaire_name.lower() == 'ghq':
            score = sum_ans - 12
            results = 'Not mention'
        elif questionnaire_name.lower() == 'bfp':
            ans_choice = []
            for answer in answers:
                ans_choice.append(int(answer['answer']))
            extr_factor = 20 + ans_choice[0] - ans_choice[5] + ans_choice[10] - ans_choice[15] + ans_choice[20] - \
                          ans_choice[25] + ans_choice[30] - ans_choice[35] + ans_choice[40] - ans_choice[45]

            agree_factor = 14 - ans_choice[1] + ans_choice[6] - ans_choice[11] + ans_choice[16] - ans_choice[21] + \
                           ans_choice[26] - ans_choice[31] + ans_choice[36] + ans_choice[41] + ans_choice[46]

            cons_factor = 14 + ans_choice[2] - ans_choice[7] + ans_choice[12] - ans_choice[17] + ans_choice[22] - \
                          ans_choice[27] + ans_choice[32] - ans_choice[37] + ans_choice[42] + ans_choice[47]

            neu_factor = 38 - ans_choice[3] + ans_choice[8] - ans_choice[13] + ans_choice[18] - ans_choice[23] - \
                         ans_choice[28] - ans_choice[33] - ans_choice[38] - ans_choice[43] - ans_choice[48]

            open_factor = 8 + ans_choice[4] - ans_choice[9] + ans_choice[14] - ans_choice[19] + ans_choice[24] - \
                          ans_choice[29] + ans_choice[34] + ans_choice[39] + ans_choice[44] + ans_choice[49]

            # print('>>>>>>', open_factor)
            # print('>>>>>>', extr_factor)
            # print('>>>>>>', agree_factor)
            # print('>>>>>>', cons_factor)
            # print('>>>>>>', neu_factor)

            score = sum(ans_choice)
            results = \
                'Openness: ' + str(open_factor) + ' Conscientiousness: ' + str(
                    cons_factor) + ' Extroversion: ' + str(extr_factor) + ' Agreeableness:' + str(
                    agree_factor) + ' Neuroticism: ' + str(neu_factor)
        else:
            score = -1
        Results.objects.create(user=request.user,
                               num_of_question_answered=answers_count,
                               duration=320,
                               score=score,
                               questionnaire=questionnaire,
                               description=results)
        return Response({'message': 'answers submitted successfully'})


class UserResults(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResultsSerializer

    def get_queryset(self):
        user = self.request.user
        return Results.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except:
            return JsonResponse({'message': 'user Not Found'}, status=404)
