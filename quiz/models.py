from django.db import models

# Create your models here.
class Quiz(models.Model):
    company_name = models.CharField(max_length=128)

class Contact(models.Model):
    name: str = models.CharField(max_length=128)
    email: str = models.EmailField()
    role: str = models.CharField(max_length=64)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL)

class Question(models.Model):
    content: str = models.CharField(max_length=256)

class QuestionOption(models.Model):
    content: str = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class QuestionAnswer(models.Model):
    content: str = models.CharField(max_length=256)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)
    user = models.ForeignKey(Contact, on_delete=models.SET_NULL)
