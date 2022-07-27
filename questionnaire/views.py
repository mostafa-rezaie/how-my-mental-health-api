from .models import Question, Questionnaires
from rest_framework.generics import ListAPIView
from .serializers import QuestionSerializer, QuestionnaireSerializer


# Create your views here.
class Questionnaire(ListAPIView):
    queryset = Question.objects.all().filter(questionnaire__name__exact='s1')
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        q1 = Questionnaires.objects.get(name='s1')
        print(q1)
        q2 = q1.question.count()
        print(q2)
        return super().get(request, *args, **kwargs)


class AllQuestionnaires(ListAPIView):
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnaireSerializer
