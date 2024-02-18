from postmarker.core import PostmarkClient
from leadanne2.schema import EmailTemplate
from leadanne2.config import SENDER_EMAIL, POSTMARK_SERVER_TOKEN


postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)


def send_email(to: str, template_id: str, data: EmailTemplate) -> None:
    postmark.emails.send_with_template(  # type: ignore
        TemplateId=template_id,
        TemplateModel=data.dict(),
        From=SENDER_EMAIL,
        To=to,
    )
