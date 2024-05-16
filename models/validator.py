import streamlit as st
import validators

def validate_url(url: str) -> bool:
    is_valid = validators.url(url)
    st.session_state["validation_error"] = False
    if not is_valid:
        st.toast('Invalid URL', icon='🚨')
        st.session_state["validation_error"] = True

def validate_email(email: str) -> bool:
    is_valid = validators.email(email)
    st.session_state["validation_error"] = False
    if not is_valid:
        st.toast('Invalid email', icon='🚨')
        st.session_state["validation_error"] = True