import logging
from PIL import Image
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

    icon = Image.open('static/icons/logo.ico')

    st.set_page_config(page_title="ElabLite",
                       layout="wide",
                       initial_sidebar_state="expanded",
                       page_icon=icon,
                       menu_items={
                           'About': 'https://github.com/CRC-Centre-Recherche-Conservation/ElabLite',
                           'Report a bug': "https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues/new?assignees=rayondemiel&labels=bug&projects=CRC-Centre-Recherche-Conservation%2F3&template=BUG-REPORT.yml&title=%5BBug%5D%3A+"
                       }
                       )

    st.title(f"ElabLite")
    st.write(
        "Welcome to ElabLite like metadata generator! This tool helps you generate metadata for use in your elabFTW instance with easy templates.")

    # init step metadata
    if "step_metadata" not in st.session_state:
        st.session_state["step_metadata"] = "step_metadata_base"
    if 'validation_error' not in st.session_state:
        st.session_state.validation_error = True
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = None

    # SIDEBAR
    menu()


if __name__ == "__main__":
    run()
