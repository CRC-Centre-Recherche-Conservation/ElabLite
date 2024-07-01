import os
import streamlit as st
import time
from datetime import datetime
from streamlit_star_rating import st_star_rating
from streamlit_tags import st_tags

from models.forms import MetadataForms
from models.technical import TechniqueOption, TECHNIQUES
from utils.manager import create_elablite
from utils.menu import menu
from utils.parser import TemplatesReader

### BASIC ###

reader = TemplatesReader(st.session_state["selected_template"])


def step_metadata_base():
    """Step 1 page - Base forms experience"""
    st.header("Experience presentation")
    if "metadata_base" not in st.session_state:
        st.session_state["metadata_base"] = None

    technique_default = None
    if st.session_state["metadata_base"] is not None:
        technique_default = st.session_state["metadata_base"]["technical"]

    with st.container(border=True):
        title = st.text_input("Title *", help="Title of the experience",
                              value=st.session_state["metadata_base"]["title"]
                              if st.session_state['metadata_base'] is not None else None)
        # Technical code
        col1, col2 = st.columns([12, 1])

        with col1:
            technical_code = st.selectbox("Select a technique *",
                                          index=list(TECHNIQUES.keys()).index(technique_default.code)
                                                if technique_default is not None else None,
                                          options=TECHNIQUES.keys(),
                                          format_func=lambda x: TECHNIQUES[x].english_name)
            if technical_code is not None:
                technical = TECHNIQUES[technical_code]
                st.info(technical)
        with col2:
            with st.container(height=11, border=False):  # css cheat button
                st.empty()
            with st.container():
                add_button = st.button(":heavy_plus_sign:", help="Add a new technique")
        if add_button:
            TechniqueOption.open_add_technique_modal()

        date = st.date_input("Date *",
                             value=st.session_state["metadata_base"]["date"]
                             if st.session_state['metadata_base'] is not None else datetime.now())
        author = st.text_input("Author *",
                               value=st.session_state["metadata_base"]["author"]
                               if st.session_state['metadata_base'] is not None else None)
        commentary = st.text_area("Commentary",
                                  value=st.session_state["metadata_base"]["commentary"]
                                  if st.session_state['metadata_base'] is not None else None)
        tags = st_tags(label="tags", maxtags=8,
                       value=st.session_state["metadata_base"]["tags"]
                       if st.session_state['metadata_base'] is not None else None)
        st.divider()
        rating = st_star_rating(label="Rate you experience", maxValue=5,
                                defaultValue=st.session_state["metadata_base"]["rating"]
                                if st.session_state['metadata_base'] is not None else 0)
        submit_enabled = all((title, date, author, technical_code))
        st.session_state["submit_enabled"] = submit_enabled
        st.session_state["metadata_base"] = {"title": title, "date": date, "author": author, "commentary": commentary,
                                             'tags': tags, 'rating': rating, 'technical': technical}


### METADATA INSTRUMENTAL ###

def step_metadata_forms():
    """Step 2 page - Metadata forms instrumental"""
    if "template_metadata" not in st.session_state:
        st.session_state["template_metadata"] = None
    st.header("Experience presentation")
    try:
        st.session_state['template_metadata'] = reader.read_metadata()
        with st.container():
            st.session_state.required_form = []
            MetadataForms.generate_form(st.session_state['template_metadata'])
            st.session_state["submit_enabled"] = all(st.session_state.required_form)
    except Exception as e:
        st.error(f"Error: {e}")
    # Re init without modification MetadataForms.generate_form()
    # To save the good template in .elablite
    st.session_state['template_metadata'] = reader.read_metadata()


### METADATA SAVING ###

def step_metadata_download():
    """Step 3 page - Metadata download to elablite format"""
    filename = st.text_input("Filename", help='Enter the filename of your metadat preset. Ex: experience name')

    if not filename.strip():
        st.session_state["submit_enabled"] = True
    else:
        st.session_state["submit_enabled"] = False

    st.download_button(
        label="Download elablite",
        data=create_elablite(metadata_base=st.session_state["metadata_base"],
                             form_data=st.session_state["form_data"],
                             template_metadata=st.session_state["template_metadata"]),
        file_name=f"{filename}.elablite",
        mime="application/octet-stream",
        disabled=st.session_state["submit_enabled"]
    )


### INTERN PAGE MANAGEMENT ###

def display_forms():
    """
    Displays forms based on the current step in the application flow.
    """
    st.info(f"""You are using the template `{st.session_state["selected_template"]}`""")
    current_step = st.session_state["step_metadata"]
    st.session_state["submit_enabled"] = False
    if current_step == "step_metadata_base":
        step_metadata_base()
    elif current_step == "step_metadata_forms":
        step_metadata_forms()
    elif current_step == "step_metadata_download":
        step_metadata_download()


def next_step():
    """
    Moves to the next step in the metadata page.
    """
    if st.session_state["step_metadata"] == "step_metadata_base":
        st.session_state["step_metadata"] = "step_metadata_forms"
    elif st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_download"


def previous_step():
    """
    Moves to the previous step in the metadata page.
    """
    if st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_base"
    elif st.session_state["step_metadata"] == "step_metadata_download":
        st.session_state["step_metadata"] = "step_metadata_forms"


### PAGE ###

st.title("Metadata Generator")
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
            if st.button("Next ⏭️", on_click=next_step,
                         disabled=not (st.session_state["submit_enabled"] and st.session_state["validation_error"])):
                pass

# redirection empty templates
else:
    st.warning("Please select/upload a template on the first page.")
    with st.spinner('Redirection'):
        time.sleep(3)
    st.switch_page("pages/1-select_template.py")
