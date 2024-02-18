import json
import logging

import sentry_sdk
import boto3
from leadanne2.config import ENV, CELERY_BROKER_URL, SENTRY_DSN
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from leadanne2.tasks import generate_result

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sentry_sdk.init(SENTRY_DSN, integrations=[AwsLambdaIntegration()], environment=ENV)

SQS = boto3.client("sqs")


def producer(event, context):
    status_code = 200
    message = ""

    if not event.get("body"):
        return {"statusCode": 400, "body": json.dumps({"message": "No body was found"})}

    try:
        message_attrs = {}
        payload = json.dumps(event["body"])
        logger.info(f"Event body: {payload}")
        SQS.send_message(
            QueueUrl=CELERY_BROKER_URL,
            MessageBody=payload,
            MessageAttributes=message_attrs,
        )
        message = "Message accepted!"
    except Exception as e:
        logger.exception("Sending message to SQS queue failed!")
        message = str(e)
        status_code = 500

    return {
        "statusCode": status_code,
        "body": json.dumps({"message": message}),
        "headers": {"Content-Type": "application/json"},
    }


def consumer(event, context):
    for record in event["Records"]:
        payload = json.loads(record["body"])

        if type(payload) == str:
            payload = json.loads(payload)

        assert type(payload) == dict

        logger.info("Message receiverd")
        generate_result(payload)
