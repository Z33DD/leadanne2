from fastapi import Request, FastAPI
from leadanne2.config import ENV, PROJECT, SENTRY_DSN
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from leadanne2.tasks import generate_result


def app_factory() -> FastAPI:

    app = FastAPI(
        title=PROJECT["name"],
        version=PROJECT["version"],
        description=PROJECT["description"],
    )
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[
            CeleryIntegration(),
            FastApiIntegration(),
        ],
        environment=ENV,
    )

    return app


app = app_factory()


@app.get("/")
def read_root():
    return {
        "name": app.title,
        "description": app.description,
        "environment": ENV,
        "vesion": app.version,
    }


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    generate_result.delay(payload)
    return {"message": "Ok"}
