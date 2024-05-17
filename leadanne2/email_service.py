import resend
from jinja2 import Environment, FileSystemLoader, select_autoescape
from leadanne2.schema import EmailTemplate
from leadanne2.config import settings, Language
from leadanne2 import logger


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

    logger.info(f"Sending email to {to}")
    resend.api_key = settings["resend_api_key"]
    params: resend.Emails.SendParams = {
        "sender": settings["sender_email"],
        "to": [to],
        "subject": subject,
        "html": html_body,
    }
    resend.Emails.send(params)


def render_html_body(data: dict, language: Language) -> str:
    logger.info(f"Rendering email template for {language}")
    env = Environment(
        loader=FileSystemLoader("templates/email"),
        autoescape=select_autoescape(),
    )
    if language == Language.PORTUGUESE:
        template = env.get_template("AI_Lead_Generation_PT.html")
    else:
        template = env.get_template("AI_Lead_Generation.html")
    return template.render(**data)
