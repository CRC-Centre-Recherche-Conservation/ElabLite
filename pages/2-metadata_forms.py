import os
import pandas as pd
import streamlit as st
import time
from datetime import datetime

from utils.menu import menu
from models.forms import MetadataForms
from utils.parser import TemplatesReader


def step_metadata_base():
    st.header("Experience presentation")
    with st.container(border=True):
        title = st.text_input("Title", help="Title of the experience")
        date = st.date_input("Date", value=datetime.now())
        author = st.text_input("Author")
        commentary = st.text_area("Commentary")
        submit_enabled = all((title, date, author))
        st.session_state["submit_enabled"] = submit_enabled


def step_metadata_forms():
    st.header("Experience presentation")
    reader = TemplatesReader(st.session_state["selected_template"])
    try:
        template_metadata = reader.read_metadata()
        with st.container():
            st.session_state.required_form = []
            MetadataForms.generate_form(template_metadata)
            st.session_state["submit_enabled"] = all(st.session_state.required_form)
    except Exception as e:
        st.error(f"Error: {e}")


def display_file_metadata(files):
    file_names = [file.name for file in files]
    df = pd.DataFrame({"File Name": file_names})
    st.data_editor(df)

def step_metadata_files():
    if "files_metadata" not in st.session_state:
        st.session_state["files_metadata"] = []
    st.header("Files metadata editor")
    st.session_state["files_metadata"] = st.file_uploader("Upload Files", accept_multiple_files=True)
    if st.session_state["files_metadata"]:
        with st.spinner("Processing..."):
            time.sleep(2)
            st.subheader("Uploaded File Names")
            display_file_metadata(st.session_state["files_metadata"])


def step_metadata_download():
    st.header("Download metadata")


def display_forms():
    st.info(f"""You are using the template `{st.session_state["selected_template"]}`""")
    current_step = st.session_state["step_metadata"]
    st.session_state["submit_enabled"] = False
    if current_step == "step_metadata_base":
        step_metadata_base()
    elif current_step == "step_metadata_forms":
        step_metadata_forms()
    elif current_step == "step_metadata_files":
        step_metadata_files()
    elif current_step == "step_metadata_download":
        step_metadata_download()


def next_step():
    if st.session_state["step_metadata"] == "step_metadata_base":
        st.session_state["step_metadata"] = "step_metadata_forms"
    elif st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_files"
    elif st.session_state["step_metadata"] == "step_metadata_files":
        st.session_state["step_metadata"] = "step_metadata_download"


def previous_step():
    if st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_base"
    elif st.session_state["step_metadata"] == "step_metadata_files":
        st.session_state["step_metadata"] = "step_metadata_forms"
    elif st.session_state["step_metadata"] == "step_metadata_download":
        st.session_state["step_metadata"] = "step_metadata_files"


### PAGE ###

st.title("View Template")
menu()

# check templates
if "selected_template" in st.session_state and os.path.exists(st.session_state["selected_template"]):

    # display page form
    display_forms()

    # buttons navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["step_metadata"] != "step_metadata_base":
            if st.button("⏮️ Previous", on_click=previous_step):
                pass
    with col2:
        if st.session_state["step_metadata"] != "step_metadata_download":
            if st.button("Next ⏭️", on_click=next_step, disabled=not st.session_state["submit_enabled"]):
                pass
        elif st.session_state["step_metadata"] == "step_metadata_forms":
            if st.button("Next ⏭️", on_click=next_step, disabled=not (st.session_state["submit_enabled"] and st.session_state["validation_error"])):
                pass

# redirection empty templates
else:
    st.warning("Please select/upload a template on the first page.")
    with st.spinner('Redirection'):
        time.sleep(3)
    st.switch_page("pages/1-select_template.py")
