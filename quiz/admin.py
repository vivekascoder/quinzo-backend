from django.contrib import admin
from quiz.models import Subject, Question, Paper

admin.site.register((Subject, Question, Paper))