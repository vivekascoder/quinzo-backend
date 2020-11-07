from django.contrib import admin
from quiz.models import Subject, Question, Paper, Quiz, QuizResult

admin.site.register((Subject, Question, Paper, Quiz, QuizResult))