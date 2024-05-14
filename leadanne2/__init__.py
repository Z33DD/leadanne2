import logging
from supabase import create_client, Client
from supabase.client import ClientOptions

from leadanne2.config import settings

logger = logging.getLogger(__name__)

logging.basicConfig(level=settings["log_level"])


def supabase_factory() -> Client:
    url = settings["supabase"]["url"]
    key = settings["supabase"]["key"]

    if not key:
        raise ValueError("SUPABASE_KEY is not set")

    return create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            schema="public",
        ),
    )


supabase = supabase_factory()
