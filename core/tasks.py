from core import postmark
from core.chatgpt import askgpt

from leadanne2.settings import EXAMPLE_RESULT, POSTMARK_SENDER_EMAIL
from leadanne2.celery import app


REFERENCE = {
    "nGpZDL": {
        "email": {
            "template_id": 33844125,
        },
        "company": {
            "name": "question_kdxbvo",
            "age": "question_Npyl4j",
            "industry": "question_q4eDY9",
            "location": "question_QKyexG",
            "size": "question_vGbXKl",
        },
        "main": {
            "Ideal customer demographics": "question_9q596V",
            "Current marketing strategies (if any)": "question_eqPQNk",
            "Unique selling points": "question_aQo5jb",
            "Short-term and long-term goals": "question_685jrJ",
            "Annual sales targets": "question_7R5L4R",
            "Specific marketing objectives": "question_b5GjNZ",
            "Marketing challenges": "question_A752Wz",
            "Competitor challenges": "question_Bz5d8K",
            "Budget constraints": "question_kdxeOe",
        },
        "contact": {
            "first_name": "question_b5GZv1",
            "email": "question_Bz5E0R",
            "last_name": "question_A75rye",
            "job_title": "question_LZyDkl",
        },
    }
}


@app.task()
def generate_result(payload: dict) -> str:
    form_id = payload["data"]["formId"]
    reference = REFERENCE[form_id]

    company_keys = [key for key in reference["company"].values()]
    main_keys = [key for key in reference["main"].values()]
    contact_keys = [key for key in reference["contact"].values()]
    all_keys = company_keys + main_keys + contact_keys

    data = {}

    for field in payload["data"]["fields"]:
        value: str = field["value"]
        field_key: str = field["key"]

        if field_key not in all_keys:
            continue

        if field["type"] in ["DROPDOWN", "MULTIPLE_CHOICE"]:
            option_id = value[0]
            value = None
            options: list[dict] = field["options"]
            i = 0
            while 1 < len(options) and not value:
                current_id = options[i]["id"]
                if current_id == option_id:
                    value = options[i]["text"]
                i += 1

        question = {"label": field["label"], "value": value}

        data.update({field["key"]: question})
    email = data[reference["contact"]["email"]]["value"]
    company_name = data[reference["company"]["name"]]["value"]
    industry = data[reference["company"]["industry"]]["value"]
    age = data[reference["company"]["age"]]["value"]
    size = data[reference["company"]["size"]]["value"]

    header = (
        f"Create a personalized marketing guide in HTML for {company_name}, the "
        f"company is in the market of {industry} for {age} years and has "
        f"arround {size} employees. They have shared their company details,"
        " target audience, goals, challenges, and unique selling points."
        " Please provide a comprehensive marketing plan that aligns with "
        "their objectives and addresses their specific needs:"
    )
    responses = []

    for label, question_id in reference["main"].items():
        answer = data[question_id]["value"]

        if type(answer) == str:
            answer = answer.strip()

        section_text = f'- {label}: "{answer}"'
        responses.append(section_text)

    prompt = "\n\n".join([header] + responses)
    prompt += f"\n\nFor example, this is a suguestion for a legal consulting agency:\n {EXAMPLE_RESULT}\n"

    reply, _ = askgpt(prompt)
    reply = reply.replace("\n", "<br />")

    postmark.emails.send_with_template(
        TemplateId=reference["email"]["template_id"],
        TemplateModel={"content": reply},
        From=POSTMARK_SENDER_EMAIL,
        To=email,
    )

    return reply
