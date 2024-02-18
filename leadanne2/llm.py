from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from leadanne2.schema import EmailTemplate
from leadanne2.config import OPENAI_API_KEY


def ask_llm(
    company_info: str, problem: str, language: str = "English"
) -> EmailTemplate:
    llm = ChatOpenAI(api_key=OPENAI_API_KEY)

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

    chain = prompt | llm | parser

    reply = chain.invoke(
        {
            "problem": problem,
            "company_info": company_info,
            "language": language,
        }
    )

    return reply
