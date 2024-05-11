from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions

from leadanne2.config import SUPABASE_URL, SUPABASE_KEY


def supabase_factory() -> Client:
    load_dotenv()
    url = SUPABASE_URL
    key = SUPABASE_KEY

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
