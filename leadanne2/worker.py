from celery import Celery
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from leadanne2.config import (
    CELERY_BROKER_URL,
    PROJECT,
    SENTRY_DSN,
    ENV,
    CELERY_RESULT_BACKEND,
)


def worker_factory() -> Celery:
    worker = Celery(
        PROJECT["name"],
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
    )
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[
            CeleryIntegration(),
            FastApiIntegration(),
        ],
        environment=ENV,
    )

    return worker


celery = worker_factory()
celery.autodiscover_tasks(["leadanne2.tasks"])
