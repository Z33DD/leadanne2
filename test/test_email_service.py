from leadanne2.email_service import (
    send_email,
    Language,
    EmailTemplate,
    render_html_body,
)


def test_send_email(example_reply: EmailTemplate) -> None:
    to = "delivered@resend.dev"
    language = Language.ENGLISH
    run_id = "12345"

    send_email(to, language, example_reply, run_id)


def test_render_html_body(snapshot, example_reply):
    payload = example_reply.dict()
    payload.update({"run_id": "12345"})

    language = Language.ENGLISH

    rendered_html = render_html_body(payload, language)

    snapshot.assert_match(rendered_html, "rendered.html")

    language = Language.PORTUGUESE

    rendered_html = render_html_body(payload, language)

    snapshot.assert_match(rendered_html, "rendered_pt.html")
