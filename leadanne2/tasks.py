from leadanne2.worker import celery
from leadanne2.llm import ask_llm
from leadanne2.email import send_email
from leadanne2.config import REFERENCE
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from leadanne2.llm import get_vector_store

TRAINING_DATA_PATH = "./training_data"


@celery.task
def generate_result(payload: dict) -> dict:
    form_id = payload["data"]["formId"]
    reference = REFERENCE[form_id]

    data = {}

    for field in payload["data"]["fields"]:
        data.update({field["key"]: field["value"]})

    email = data[reference["fields"]["email"]]
    company_information = data[reference["fields"]["company_information"]]
    problem = data[reference["fields"]["problem"]]

    reply = ask_llm(company_information, problem, reference["language"])

    send_email(email, reference["template_id"], reply)

    return reply.dict()


@celery.task
def training():
    store = get_vector_store()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for file_name in os.listdir(TRAINING_DATA_PATH):
        loader = PyPDFLoader(f"{TRAINING_DATA_PATH}/{file_name}")
        docs = loader.load()
        store.add_documents(splitter.split_documents(docs))
