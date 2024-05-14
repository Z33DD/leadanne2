from celery import Celery
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from leadanne2.config import project, settings


def worker_factory() -> Celery:
    worker = Celery(
        project["name"],
        broker=settings["broker_url"],
    )
    if settings["sentry_dsn"]:
        sentry_sdk.init(
            settings["sentry_dsn"],
            integrations=[
                CeleryIntegration(),
                FastApiIntegration(),
            ],
            environment=settings.env,
        )

    return worker


celery = worker_factory()
celery.autodiscover_tasks(["leadanne2.tasks"])
