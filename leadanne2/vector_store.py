from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores.supabase import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

from leadanne2 import supabase
from leadanne2.config import settings


def vector_store_factory() -> VectorStore:
    if settings.openai_api_key:
        embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
    else:
        embeddings = OllamaEmbeddings(model=settings.llm_model)
    store = SupabaseVectorStore(
        client=supabase,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents",
    )

    return store


vstore = vector_store_factory()


def add_pdf_document(path: str) -> None:
    loader = PyPDFLoader(file_path=path)
    raw_docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(raw_docs)

    vstore.add_documents(docs)


def add_webpage_document(urls: list[str]) -> None:
    loader = AsyncChromiumLoader(urls)
    html = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        html, tags_to_extract=["p", "li", "div", "a"]
    )
    docs = [doc for doc in docs_transformed]
    vstore.add_documents(docs)
