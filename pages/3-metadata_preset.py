import os
from time import sleep
import streamlit as st

from utils.menu import menu
from utils.manager import manage_temp_dir

st.title("Upload or Select preset/template")
menu()
option = st.sidebar.radio("Options", ["Upload experiment", "Select existing experiment"])
st.sidebar.divider()
templates_dir = manage_temp_dir(child='presets')
st.markdown("""
This page lets you select a completed experiment and its metadata. Format: ELABLITE
- `Upload experiment`: Import a new experiment.
- `Select existing experiment`: Use a experiment save already loaded in memory (valid until next reboot).
""")


### OPTIONS ###
if option == "Upload experiment":
    uploaded_file = st.file_uploader("Upload a file",
                                     type=["elablite"],
                                     accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state["selected_preset"] = os.path.join(templates_dir, uploaded_file.name)
        # Save the uploaded file to the temporary directory
        with open(st.session_state["selected_preset"], "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        # re init
        st.session_state['metadata_base'] = None
        st.session_state['template_metadata'] = None
        st.session_state['form_data'] = None
        # var
        st.session_state["preset_metadata"] = "preset_metadata_base"
        st.session_state.form_data = {}
        # redirect
        sleep(1.5)
        st.switch_page("pages/4-metadata_management.py")
elif option == "Select existing experiment":
    templates = os.listdir(templates_dir)
    selected_template = st.selectbox("Select a recent experience", templates,
                                     index=None, placeholder="Choosing ...")
    if st.button('Validate'):
        try:
            # re init
            st.session_state['metadata_base'] = None
            st.session_state['template_metadata'] = None
            st.session_state['form_data'] = None
            # var
            st.session_state["selected_preset"] = os.path.join(templates_dir, selected_template)
            st.session_state["preset_metadata"] = "preset_metadata_base"
            st.session_state.form_data = {}
            # redirect
            st.switch_page("pages/4-metadata_management.py")
        except TypeError:
            st.warning("You need to select an experience")
