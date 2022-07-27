from django.contrib import admin
from .models import Questionnaires,Question,Answers

# Register your models here.
admin.site.register(Questionnaires)
admin.site.register(Question)
admin.site.register(Answers)
