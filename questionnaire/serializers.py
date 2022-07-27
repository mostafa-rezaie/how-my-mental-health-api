from rest_framework import serializers
from .models import Question, Questionnaires


class QuestionSerializer(serializers.ModelSerializer):
    questionnaire_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = ['questionnaire_name', 'question_type', 'title', ]

    def get_questionnaire_name(self, obj):
        return obj.questionnaire.name


class QuestionnaireSerializer(serializers.ModelSerializer):
    question_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Questionnaires
        fields = ['name', 'question_number']

    def get_question_number(self, obj):
        return obj.question.count()
