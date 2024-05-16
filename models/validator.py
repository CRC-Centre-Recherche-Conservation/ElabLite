import streamlit as st
import validators
from validators import ValidationError

def validate_url(url: str) -> bool:
    is_valid = validators.url(url)
    if not is_valid:
        st.toast('Invalid URL', icon='🚨')
        st.session_state["submit_enabled"] = False

def validate_email(email: str) -> bool:
    is_valid = validators.email(email)
    if not is_valid:
        st.toast('Invalid email', icon='🚨')
        st.session_state["submit_enabled"] = False