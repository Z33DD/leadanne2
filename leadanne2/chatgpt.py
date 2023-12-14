from openai import OpenAI

from leadanne2.settings import OPENAI_KEY


def askgpt(question, chat_log=None):
    if chat_log is None:
        chat_log = [
            {
                "role": "system",
                "content": "You are a helpful, upbeat and funny assistant.",
            }
        ]
    # chat_log.append({"role": "user", "content": question})

    client = OpenAI(api_key=OPENAI_KEY)

    # response = completion.create(model="gpt-3.5-turbo", messages=chat_log)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # prompt=question,
        messages=chat_log,
    )

    return completion.choices[0].message.content
