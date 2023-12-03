from core.tasks import generate_result
import json

with open("webhook_payload_pt.json", "r") as fp:
    webhook_payload = json.load(fp)

rst = generate_result(webhook_payload)

print(rst)
