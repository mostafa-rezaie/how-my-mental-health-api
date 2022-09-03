from pyexpat import model
from django.db import models
from profile_api.models import UserProfile


# Create your models here.

class Questionnaires(models.Model):
    name = models.CharField(max_length=40, unique=True)
    date_created = models.DateField(auto_now=True)
    description = models.TextField(default='decs', null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Question(models.Model):
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['id']

    TYPE = ((2, 'Two Choice'), (3, 'Three Choice'), (4, 'Four Choice'), (5, 'Five Choice'))

    questionnaire = models.ForeignKey(Questionnaires, related_name='question', on_delete=models.CASCADE)
    question_type = models.IntegerField(choices=TYPE, default=5)
    title = models.CharField(max_length=255, verbose_name='Title')
    is_active = models.BooleanField(default=True, verbose_name='Active Status')
    qid = models.IntegerField(null=True)

    # TODO:add word length for each question

    def __str__(self):
        return self.title


class Answers(models.Model):
    class Meta:
        ordering = ['id']

    TYPE = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    user = models.ForeignKey(UserProfile, related_name='answer', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE)
    answer = models.IntegerField(choices=TYPE, verbose_name='Answer Choice')


class Results(models.Model):
    class Meta:
        ordering = ['id']

    user = models.ForeignKey(UserProfile, related_name='result', on_delete=models.CASCADE)
    num_of_question_answered = models.IntegerField()
    duration = models.IntegerField(verbose_name='duration(s)')
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    questionnaire = models.ForeignKey(Questionnaires,
                                      related_name='results',
                                      on_delete=models.CASCADE,
                                      to_field='name',
                                      default='s1')
