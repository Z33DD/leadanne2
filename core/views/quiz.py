from django.http import HttpRequest, JsonResponse
import json

from core.models import Contact, QuestionOption, Quiz, Question
from django.forms.models import model_to_dict


def post(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSONDecodeError"})

    quiz = Quiz(company_name=payload["company"]["name"])
    quiz.save()
    contact = Contact(
        name=payload["contact"]["name"],
        email=payload["contact"]["email"],
        role=payload["contact"]["role"],
        quiz=quiz,
    )
    contact.save()

    questions = Question.objects.all().order_by("index")
    options = QuestionOption.objects.all()

    questions_data = []

    for question in questions:
        options_data = []
        for option in options:
            if option.question.id == question.id:
                option_data = model_to_dict(option)
                del option_data["question"]
                options_data.append(option_data)
        question_data = {
            "content": question.content,
            "options": options_data,
        }
        questions_data.append(question_data)

    return JsonResponse(
        {
            "contact": contact.id,
            "quiz": quiz.id,
            "questions": questions_data,
        }
    )
