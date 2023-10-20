from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import Contact, Question, QuestionAnswer, QuestionOption, Quiz


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "company_name"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "role"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "index", "content"]


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "content"]


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ["id", "question", "option", "quiz", "contact", "content"]
