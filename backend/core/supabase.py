from supabase import create_client
from core.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

from supabase import create_client
from core.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_authed_client(token: str):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(token)
    return client