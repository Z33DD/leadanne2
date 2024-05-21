from operator import itemgetter
from typing import Optional
from uuid import uuid4
from fastapi.logger import logger
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from leadanne2.schema import EmailTemplate
from leadanne2.config import settings
from leadanne2 import supabase

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.exceptions import OutputParserException
from leadanne2.utils import retry_on_exception
from leadanne2.vector_store import vstore


def get_model(debug: Optional[bool] = False) -> BaseChatModel:
    model = settings["llm_model"]
    if settings["openai_api_key"]:
        llm = ChatOpenAI(
            api_key=settings["openai_api_key"],
            model=model,
        )
        logger.info(f"Using {model} from OpenAI")
    else:
        logger.info(f"Using {model} from Ollama")
        llm = Ollama(model=model)
    return llm


@retry_on_exception(OutputParserException)
def ask_llm(
    company_info: str,
    problem: str,
    language: Optional[str] = "English",
    debug: Optional[bool] = False,
) -> tuple[EmailTemplate, str]:
    llm = get_model(debug)

    parser = PydanticOutputParser(pydantic_object=EmailTemplate)
    prompt = PromptTemplate(
        template=(
            "You are a marketer."
            "Your task is to write a answer to a "
            "users problem given a context.\n"
            "Translate to {language}, if necessary.\n"
            "{format_instructions}\n"
            "Here is the user problem:\n"
            "{problem}\n"
            "Here is the context:\n"
            "{company_info}\n"
            "{context}\n"
        ),
        input_variables=["problem", "company_info", "language"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )

    retriever = vstore.as_retriever(search_kwargs={"k": 3})
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

    run_id = uuid4()
    reply = chain.invoke(
        {
            "problem": problem,
            "company_info": company_info,
            "language": language,
        },
        config={"metadata": {"run_id": run_id}},
    )

    new_entry = {
        "id": str(run_id),
        "problem": problem,
        "company_info": company_info,
        "language": language,
    }
    supabase.table("LLM Runs").insert(new_entry).execute()
    logger.debug(f"LLM run ID: {run_id}")

    return reply, str(run_id)
