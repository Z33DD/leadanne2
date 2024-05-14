from typing import Optional
import typer
import uvicorn
from leadanne2.vector_store import add_pdf_document, add_webpage_document
from leadanne2.worker import celery
from leadanne2.config import settings
import urllib.parse
import os


app = typer.Typer()


@app.command(help="Run the server.")
def serve(port: int = 8000, log_level: Optional[str] = None):
    if log_level is None:
        log_level = settings["log_level"]
    server = uvicorn.Server(
        uvicorn.Config(
            app="leadanne2.server:app",
            port=port,
            log_level=log_level,
            use_colors=True,
            reload=True,
        )
    )
    server.run()


@app.command(help="Run the celery worker.")
def work():
    worker = celery.Worker(include=["leadanne2.tasks"])
    worker.start()


@app.command(help="Add a PDF or URL document to the vector store.")
def add_doc(address: str):
    if os.path.isfile(address):
        add_pdf_document(address)
    else:
        parsed_url = urllib.parse.urlparse(address)
        if parsed_url.scheme and parsed_url.netloc:
            add_webpage_document([address])
        else:
            raise ValueError("It should be a file path or a URL.")


@app.command(help="Add docs to the vector store.")
def train(directory: str = "./training_data"):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith(".pdf"):
            print(f"Adding {filepath}")
            add_pdf_document(filepath)
    links_path = directory + "/links.txt"
    if os.path.isfile(links_path):
        print(f"Adding webpages from {links_path}")
        with open(links_path) as f:
            links = f.readlines()
        add_webpage_document(links)


if __name__ == "__main__":
    app()
