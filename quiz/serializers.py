from rest_framework import serializers
from quiz.models import Subject, Question, Paper, Quiz, QuizResult
from django.contrib.auth import password_validation
from rest_framework import validators
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def validate(self, data):
        if len(data['username']) < 7:
            raise serializers.ValidationError("The username length should be at least 8.")
        try:
            password_validation.validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError(e)
        return data
    
    def create(self, validated_data):
        return User.objects.create_user(
            username = validated_data.get('username'),
            password = validated_data.get('password'),
            email = validated_data.get('email', ''),
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', '')
        )
    

        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        depth = 1

class QuizResultSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = QuizResult
        fields = '__all__'
    
    def create(self, validated_data):
        # user = CurrentUserDefault()
        return QuizResult(**validated_data)

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
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)