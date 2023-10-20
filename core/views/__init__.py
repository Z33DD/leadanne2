from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.models import Question, QuestionOption, QuestionAnswer
from core.serializers import (
    QuestionAnswerSerializer,
    QuestionOptionSerializer,
    QuestionSerializer,
)


class QuestionOptionList(generics.ListCreateAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer
    permission_classes = (AllowAny,)


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)


class AnswerCraate(generics.CreateAPIView):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer
    permission_classes = (AllowAny,)
