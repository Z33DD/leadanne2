from django.contrib import admin
from core.models import Quiz, Contact, Question, QuestionOption, QuestionAnswer


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    pass
