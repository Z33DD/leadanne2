import json
from leadanne2.chatgpt import askgpt
from functools import lru_cache
from leadanne2.settings import BASE_DIR, POSTMARK_SENDER_EMAIL, POSTMARK_SERVER_TOKEN
from markdown import markdown
from postmarker.core import PostmarkClient

postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)


REFERENCE = {
    "nGpZDL": {
        "email": {
            "template_id": 33844125,
            "language": "English",
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
    },
    "wQ7k87": {
        "email": {
            "template_id": 34025381,
            "language": "Portuguese",
        },
        "company": {
            "name": "question_A7R5eB",
            "age": "question_KY2yKM",
            "industry": "question_LZxyLG",
            "location": "question_pbq9pV",
            "size": "question_Bzo5W7",
        },
        "main": {
            "Ideal customer demographics": "question_1A05oM",
            "Current marketing strategies (if any)": "question_MeZypY",
            "Unique selling points": "question_gDPr6N",
            "Short-term and long-term goals": "question_yPAk50",
            "Annual sales targets": "question_XxAyPO",
            "Specific marketing objectives": "question_81D54A",
            "Marketing challenges": "question_0Q05RZ",
            "Competitor challenges": "question_zxBv51",
            "Budget constraints": "question_5B05PM",
        },
        "contact": {
            "first_name": "question_6805Ee",
            "email": "question_b5RGQe",
            "last_name": "question_7R05rL",
            "job_title": "question_vG6b5A",
        },
    },
}


@lru_cache(maxsize=None)
def get_conversation_context():
    with open(str(BASE_DIR) + "/context.json", "r") as fp:
        content = json.load(fp)
    return content


def generate_result(payload: dict) -> str:
    form_id = payload["data"]["formId"]
    reference = REFERENCE[form_id]

    company_keys = [key for key in reference["company"].values()]
    main_keys = [key for key in reference["main"].values()]
    contact_keys = [key for key in reference["contact"].values()]
    language = reference["email"]["language"]
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
        f"Create a personalized marketing guide in {language} for {company_name}, the "
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

    reply = askgpt(
        prompt,
        chat_log=get_conversation_context(),
    )
    reply = markdown(reply)

    # postmark.emails.send_with_template(
    #     TemplateId=reference["email"]["template_id"],
    #     TemplateModel={"content": reply},
    #     From=POSTMARK_SENDER_EMAIL,
    #     To=email,
    # )

    return reply
