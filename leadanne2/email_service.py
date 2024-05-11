import resend
from jinja2 import Environment, FileSystemLoader, select_autoescape
from leadanne2.schema import EmailTemplate
from leadanne2.config import RESEND_API_KEY
from enum import Enum


class Language(Enum):
    PORTUGUESE = "Portuguese"
    ENGLISH = "English"


def send_email(
    to: str,
    language: Language,
    data: EmailTemplate,
    run_id: str,
) -> None:
    payload = data.dict()
    payload.update({"run_id": run_id})

    if language == Language.PORTUGUESE:
        subject = "Seus dicas de marketing estão prontas!"
    else:
        subject = "Your AI marketing tips are ready!"

    html_body = render_html_body(payload, language)

    resend.api_key = RESEND_API_KEY
    params: resend.Emails.SendParams = {
        "sender": "Codetta Tech <leadanne2@mail.z33dd.com>",
        "to": [to],
        "subject": subject,
        "html": html_body,
    }
    resend.Emails.send(params)


def render_html_body(data: dict, language: Language) -> str:
    env = Environment(
        loader=FileSystemLoader("templates/email"),
        autoescape=select_autoescape(),
    )
    print(env.list_templates())
    if language == Language.PORTUGUESE:
        template = env.get_template("AI_Lead_Generation_PT.html")
    else:
        template = env.get_template("AI_Lead_Generation.html")
    return template.render(**data)
