import streamlit as st

def menu():
    """
    Menu sidebar
    """
    st.sidebar.image('static/icons/logo.svg')
    st.sidebar.title("ElabLite")
    st.sidebar.page_link("app.py", label="Homepage")
    st.sidebar.title("Metadata")
    st.sidebar.page_link("pages/1-select_template.py", label="Select template")
    if "selected_template" in st.session_state and st.session_state["selected_template"] is not None:
        st.sidebar.page_link("pages/2-metadata_forms.py", label="Complete metadata")
    st.sidebar.divider()