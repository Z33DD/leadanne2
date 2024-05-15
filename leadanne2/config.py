from pathlib import Path
import tomllib

from enum import Enum
from dynaconf import Dynaconf
from dotenv import load_dotenv

load_dotenv()
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        "../settings.yaml",
        "../.secrets.yaml",
        "/app/settings.yaml",
        "/app/.secrets.yaml",
    ],
    environments=True,
)


def get_project_config() -> dict:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["tool"]["poetry"]


project = get_project_config()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Language(Enum):
    PORTUGUESE = "Portuguese"
    ENGLISH = "English"
