from django.http import HttpRequest, JsonResponse
import json

from core.tasks import generate_result


def post(request: HttpRequest) -> tuple[JsonResponse, int]:
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSONDecodeError"},
        )

    generate_result.delay(payload)

    return JsonResponse({"message": f"We will send the results to your email!"})
