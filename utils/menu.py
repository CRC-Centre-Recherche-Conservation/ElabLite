import streamlit as st

from __version__ import __identifier__ as VERSION


def menu():
    """
    Menu sidebar
    """
    st.markdown(
        '''
        <style>
        [data-testid="stSidebar"] [data-testid="stExpander"] details {
        border: none !important;
        }
        [data-testid="stSidebar"] div[data-testid="stExpander"] details summary p {
        font-size: 2rem;
        font-weight: bold;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )
    with st.sidebar.container():
        st.sidebar.image('static/icons/logo.svg')
        st.sidebar.markdown(f"<p style='text-align:center'><i>Version: {VERSION}</i></p>", unsafe_allow_html=True)
    with st.sidebar.container():
        st.sidebar.page_link("app.py", label="Homepage", icon="🏠")
    with st.sidebar.expander("Experiment Menu", expanded=True):
        st.subheader("Metadata Experiment")
        st.page_link("pages/1-select_template.py", label="• New Experiment")
        st.page_link("pages/1-load_template.py", label="• Load Experiment")
        if "selected_template" in st.session_state and st.session_state["selected_template"] is not None:
            st.page_link("pages/2-metadata_forms.py", label="• Current Experiment")
        st.subheader("Files Experiment")
        st.page_link("pages/3-metadata_preset.py", label="• Select Experiment")
        if "selected_preset" in st.session_state and st.session_state["selected_preset"] is not None:
            st.page_link("pages/4-metadata_management.py", label="• Complete Experiment(s)")
    st.sidebar.divider()
    st.session_state['temporary_container'] = st.sidebar.container()
