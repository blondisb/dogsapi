from django.conf import settings
from supabase import create_client

def get_supabase():
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)