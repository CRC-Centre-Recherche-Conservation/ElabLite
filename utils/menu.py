import streamlit as st

from __version__ import __identifier__ as VERSION

def menu():
    """
    Menu sidebar
    """
    with st.sidebar.container():
        st.sidebar.image('static/icons/logo.svg')
        st.sidebar.markdown(f"<p style='text-align:center'><i>Version: {VERSION}</i></p>", unsafe_allow_html=True)
    with st.sidebar.container():
        st.sidebar.title("ElabLite")
        st.sidebar.page_link("app.py", label="Homepage")
        st.sidebar.title("Metadata")
        st.sidebar.page_link("pages/1-select_template.py", label="Select template")
        if "selected_template" in st.session_state and st.session_state["selected_template"] is not None:
            st.sidebar.page_link("pages/2-metadata_forms.py", label="Complete metadata")
        st.sidebar.divider()