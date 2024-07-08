import os
from time import sleep
import streamlit as st

from utils.menu import menu
from utils.manager import manage_temp_dir

st.title("Upload or Select Template")
menu()
option = st.sidebar.radio("Options", ["Upload Template", "Select existing template"])
st.sidebar.divider()
templates_dir = manage_temp_dir()
st.markdown("""
This page allows you to use an authority form template from an electronic laboratory notebook to acquire metadata about 
one or more experiences. Format: JSON, CSV, ELN
- `Upload Template`: Import a new template
- `Select Existing Template`: Use a template already loaded in memory (valid until next reboot).
""")

### OPTIONS ###
if option == "Upload Template":
    uploaded_file = st.file_uploader("Upload a file", type=["json", "csv", "eln"], accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state["selected_template"] = os.path.join(templates_dir, uploaded_file.name)
        # Save the uploaded file to the temporary directory
        with open(st.session_state["selected_template"], "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        # var
        st.session_state["step_metadata"] = "step_metadata_base"
        st.session_state['metadata_base'] = {}
        st.session_state['template_metadata'] = None
        st.session_state['form_data'] = {}
        # redirect
        sleep(1.5)
        st.switch_page("pages/2-metadata_forms.py")
elif option == "Select existing template":
    templates = os.listdir(templates_dir)
    templates.remove('presets')
    selected_template = st.selectbox("Select a recent template", templates, index=None, placeholder="Choosing ...")
    if st.button('Validate'):
        try:
            # var
            st.session_state["selected_template"] = os.path.join(templates_dir, selected_template)
            st.session_state["step_metadata"] = "step_metadata_base"
            st.session_state['metadata_base'] = {}
            st.session_state['template_metadata'] = None
            st.session_state['form_data'] = {}
            # redirect
            st.switch_page("pages/2-metadata_forms.py")
        except TypeError:
            st.warning("You need to select a template")
