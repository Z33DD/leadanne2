from leadanne2.worker import celery
from leadanne2.llm import ask_llm
from leadanne2.email_service import send_email
from leadanne2.config import REFERENCE


@celery.task
def generate_result(payload: dict) -> dict:
    form_id = payload["data"]["formId"]
    reference = REFERENCE[form_id]

    data = {}

    for field in payload["data"]["fields"]:
        data.update({field["key"]: field["value"]})

    email = data[reference["fields"]["email"]]
    company_information = data[reference["fields"]["company_information"]]
    problem = data[reference["fields"]["problem"]]

    reply, run_id = ask_llm(
        company_information,
        problem,
        reference["language"],
    )

    send_email(
        email,
        reference["template_id"],
        reply,
        run_id,
    )

    return reply.dict()
