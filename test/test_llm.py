from leadanne2.llm import ask_llm


def test_ask_llm():
    company_info = (
        "Codetta Tech is a marketing company focused on creating "
        "custom made websites and social media management."
    )
    problem = "How can we increase our customer engagement?"
    language = "English"
    debug = False

    reply = ask_llm(company_info, problem, language, debug)

    assert reply
