import pprint
from typing import Optional
import typer
import uvicorn

from leadanne2.llm import ask_llm
from leadanne2.tasks import training
from leadanne2.worker import celery

app = typer.Typer()


@app.command(help="Run the server.")
def serve():

    server = uvicorn.Server(
        uvicorn.Config(
            "leadanne2.server:app",
            port=8000,
            use_colors=True,
            reload=True,
        )
    )
    server.run()


@app.command(help="Run the worker.")
def worker():
    argv = [
        "worker",
    ]
    celery.worker_main(argv)


@app.command(help="Invoke the LLM.")
def invoke(
    company: str,
    problem: str,
    language: Optional[str] = None,
):
    answer = ask_llm(
        company_info=company,
        problem=problem,
        language=language,
        debug=True,
    )

    pprint.pp(answer)


@app.command(help="Add documents to vector store.")
def train():
    training.apply()


if __name__ == "__main__":
    app()
