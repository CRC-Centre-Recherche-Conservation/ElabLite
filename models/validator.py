import streamlit as st
import validators

def validate_url(url: str) -> bool:
    """
        Validates the format of a URL.

        Args:
            url (str): The URL to be validated.

        Returns:
            bool: True if the URL is valid, False otherwise.

        Rapid Doc:
        Validates the format of the given URL using the `validators.url()` function.
        If the URL is invalid, displays a toast message indicating an invalid URL and sets a session state variable 'validation_error' to True.

        Example:
            is_valid = validate_url('https://example.com')
    """
    is_valid = validators.url(url)
    st.session_state["validation_error"] = False
    if not is_valid:
        st.toast('Invalid URL', icon='🚨')
        st.session_state["validation_error"] = True

def validate_email(email: str) -> bool:
    """
        Validates the format of an email address.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email address is valid, False otherwise.

        Rapid Doc:
        Validates the format of the given email address using the `validators.email()` function.
        If the email is invalid, displays a toast message indicating an invalid email and sets a session state variable 'validation_error' to True.

        Example:
            is_valid = validate_email('example@email.com')
    """
    is_valid = validators.email(email)
    st.session_state["validation_error"] = False
    if not is_valid:
        st.toast('Invalid email', icon='🚨')
        st.session_state["validation_error"] = True