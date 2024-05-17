from fastapi import Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from leadanne2 import supabase, logger
from leadanne2.config import project, settings
from leadanne2.tasks import generate_result

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


def app_factory() -> FastAPI:
    app = FastAPI(
        title=project["name"],
        version=project["version"],
        description=project["description"],
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

    return app


app = app_factory()


@app.get("/")
def read_root():
    return {
        "name": app.title,
        "description": app.description,
        "environment": settings.env,
        "version": app.version,
        "docs": app.docs_url,
    }


@app.post("/webhook")
async def webhook(request: Request):
    logger.info("Received webhook request")
    payload = await request.json()
    generate_result.delay(payload)
    return {"message": "Ok"}


templates = Jinja2Templates(directory="templates")


@app.get("/rate/{run_id}", response_class=HTMLResponse)
def rate_a_llm_reply(
    request: Request,
    run_id: str,
    rating: int | None = None,
) -> _TemplateResponse:
    if not rating:
        return templates.TemplateResponse(
            request=request,
            name="rating.html",
            context={
                "rate": 0,
                "run_id": run_id,
            },
        )

    table = supabase.table("Ratings")
    payload = {"rate": rating, "run_id": run_id}

    data, _ = table.select("count").eq("run_id", run_id).execute()
    count = data[1][0]["count"]

    if not count:
        table.insert(payload).execute()
    else:
        table.update(payload).eq("run_id", run_id).execute()

    return templates.TemplateResponse(
        request=request,
        name="rating.html",
        context=payload,
    )
