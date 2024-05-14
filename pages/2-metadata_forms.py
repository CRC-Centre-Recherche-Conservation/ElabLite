
import os
import streamlit as st
import time

from utils.menu import menu
from models.forms import MetadataForms
from utils.parser import TemplatesReader


st.title("View Template")
menu()

if "selected_template" in st.session_state and os.path.exists(st.session_state["selected_template"]):
    reader = TemplatesReader(st.session_state["selected_template"])
    st.info(f"""You are using the template `{st.session_state["selected_template"]}`""")

    try:
        template_metadata = reader.read_metadata()
        MetadataForms.generate_form(template_metadata)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please select/upload a template on the first page.")
    with st.spinner('Redirection'):
        time.sleep(3)
    st.switch_page("pages/1-select_template.py")

