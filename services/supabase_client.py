import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def _get_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])


supabase: Client = _get_client()
