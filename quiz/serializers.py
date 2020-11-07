from rest_framework import serializers
from quiz.models import Subject, Question, Paper


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Subject

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Paper


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = [
            'title',
            'options',
            'subject', 
            'marks',
            'answer',
            'date'
        ]
        read_only_fields = ['answer', 'marks', 'date']

    def get_options(self, obj):
        return {
            'option_a': obj.option_a,
            'option_b': obj.option_b,
            'option_c': obj.option_c,
            'option_d': obj.option_d
        }
        
