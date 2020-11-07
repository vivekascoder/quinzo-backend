from django.shortcuts import render
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
from quiz.serializers import (
    Subject, Question,
    QuestionSerializer, SubjectSerializer,
    Paper, PaperSerializer
)

class QuestionPage(pagination.BasePagination):
    page_size = 20

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = [authentication.TokenAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = QuestionPage



class ByQuestion(views.APIView):
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

class PaperViews(ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer