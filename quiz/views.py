from django.shortcuts import render, get_object_or_404
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
import django.contrib.auth.password_validation as validators
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from quiz.serializers import (
    Subject, Question,
    QuestionSerializer, SubjectSerializer,
    Paper, PaperSerializer, LoginSerializer,
    UserSerializer, User,
    Quiz, QuizSerializer
)

class QuestionPage(pagination.BasePagination):
    page_size = 20

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    # authentication_classes = [authentication.TokenAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = QuestionPage



class ByQuestion(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        try:
            subject = Subject.objects.get(pk=id)
        except Subject.DoesNotExist:
            return Response({'error': 'Does Not Exist.'}, status=status.HTTP_404_NOT_FOUND)

        queryset = subject.questions.all()
        serializer = QuestionSerializer(instance=queryset, many=True)
        return Response(serializer.data)

class SubjectViews(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaperViews(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username', None)
            password = serializer.validated_data.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    t = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    t = Token.objects.create(user=user)
                auth_token = t.key
                return Response({'message': "You're logged in.", 'token': auth_token})
            else:
                return Response({'error': "Correct credentials were not provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class LogoutView(views.APIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': "You're logout"})
        else:
            return Response({'error': 'Not Logged In.'})

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

class QuizView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, test_id):
        test = get_object_or_404(Quiz, pk=test_id)
        current_time = timezone.now()

        if current_time >= test.starting_time and current_time <= test.ending_time:
            serilizer = QuizSerializer(instance=test)
            return Response(serilizer.data)
        else:
            return Response({'error': 'The Test Does\'t started or has been ended.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
