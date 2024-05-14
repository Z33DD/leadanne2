from leadanne2.worker import celery
from leadanne2.llm import ask_llm
from leadanne2 import logger
from leadanne2.email_service import send_email
from leadanne2.config import settings


@celery.task
def generate_result(payload: dict) -> dict:
    logger.info("Starting LLM task")
    form_id = payload["data"]["formId"]
    reference = settings["reference"][form_id]

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
        reference["language"],
        reply,
        run_id,
    )

    return reply.dict()
