import logging
import streamlit as st

from utils.menu import menu

# Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    """
    Run app - homepage
    :return:
    """
    st.set_page_config(page_title="ElabLite", )
    st.title(f"ElabLite")
    st.write(
        "Welcome to ElabLite like metadata generator! This tool helps you generate metadata for use in your elabFTW instance with easy templates.")

    # init step metadata
    if "step_metadata" not in st.session_state:
        st.session_state["step_metadata"] = "step_metadata_base"
    if 'validation_error' not in st.session_state:
        st.session_state.validation_error = True

    # SIDEBAR
    menu()


if __name__ == "__main__":
    run()
