# app/database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def get_db() -> Client:
    """Get Supabase client instance"""
    supabase: Client = create_client(url, key)
    return supabase