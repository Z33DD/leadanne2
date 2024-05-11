import json
import pytest

from leadanne2.schema import EmailTemplate


@pytest.fixture
def example_reply() -> EmailTemplate:
    path = "test/example_reply.json"
    with open(path) as file:
        data = json.load(file)
    return EmailTemplate(**data)
