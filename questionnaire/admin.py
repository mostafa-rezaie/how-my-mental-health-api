from django.contrib import admin
from .models import Questionnaires, Question, Answers, Results


class ResultsAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


# Register your models here.
admin.site.register(Questionnaires)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Results, ResultsAdmin)
