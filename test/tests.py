import json

from leadanne2.chatgpt import askgpt
from leadanne2.tasks import generate_result

with open("test/webhook_payload_pt.json", "r") as fp:
    webhook_payload = json.load(fp)

# askgpt("Hello!")
reply = generate_result(webhook_payload)
print(reply)
