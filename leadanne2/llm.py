from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from leadanne2.schema import EmailTemplate
from leadanne2.config import OPENAI_API_KEY, DEBUG
from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from operator import itemgetter
import chromadb
from langchain_core.language_models.chat_models import BaseChatModel


def get_model(debug: Optional[bool] = False) -> BaseChatModel:
    if DEBUG or debug:
        print("Using Ollama")
        llm = Ollama(model="llama2")
    else:
        print("Using OpenAI")
        llm = ChatOpenAI(api_key=OPENAI_API_KEY)
    return llm


def get_vector_store() -> VectorStore:
    client = chromadb.HttpClient(
        host="localhost",
        port=8001,
    )
    store = Chroma(embedding_function=OpenAIEmbeddings(), client=client)

    return store


def ask_llm(
    company_info: str,
    problem: str,
    language: Optional[str] = "English",
    debug: Optional[bool] = False,
) -> EmailTemplate:
    llm = get_model(debug)

    parser = PydanticOutputParser(pydantic_object=EmailTemplate)
    prompt = PromptTemplate(
        template=(
            "You are a world class marketer."
            "Provide solutions to the user's problem.\n"
            "Translate to {language}, if necessary.\n"
            "{format_instructions}\n"
            "{company_info}\n"
            "{problem}\n"
        ),
        input_variables=["problem", "company_info", "language"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    vector_store = get_vector_store()
    retriever = vector_store.as_retriever()
    chain = (
        {
            "context": itemgetter("problem") | retriever,
            "problem": itemgetter("problem"),
            "company_info": itemgetter("company_info"),
            "language": itemgetter("language"),
        }
        | prompt
        | llm
        | parser
    )

    reply = chain.invoke(
        {
            "problem": problem,
            "company_info": company_info,
            "language": language,
        }
    )

    return reply
