from django.contrib import admin
from .models import Questionnaires, Question, Answers, Results


class ResultsAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


class QuestionnaireAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(Questionnaires,QuestionnaireAdmin)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Results, ResultsAdmin)
