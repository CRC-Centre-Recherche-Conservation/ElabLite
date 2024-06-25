import os
from time import sleep
import streamlit as st

from utils.menu import menu
from utils.manager import manage_temp_dir

st.title("Upload or Select preset/template")
menu()
option = st.sidebar.radio("Options", ["Upload preset", "Select existing preset"])
st.sidebar.divider()
templates_dir = manage_temp_dir(child='presets')

### OPTIONS ###
if option == "Upload preset":
    uploaded_file = st.file_uploader("Upload a file",
                                     type=["json", "csv", "eln", "elablite"],
                                     accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state["selected_preset"] = os.path.join(templates_dir, uploaded_file.name)
        # Save the uploaded file to the temporary directory
        with open(st.session_state["selected_preset"], "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        # var
        st.session_state["preset_metadata"] = "preset_metadata_base"
        st.session_state.form_data = {}
        # redirect
        sleep(1.5)
        st.switch_page("pages/4-metadata_management.py")
elif option == "Select existing preset":
    templates = os.listdir(templates_dir)
    selected_template = st.selectbox("Select a recent preset/template", templates,
                                     index=None, placeholder="Choosing ...")
    if st.button('Validate'):
        try:
            # var
            st.session_state["selected_preset"] = os.path.join(templates_dir, selected_template)
            st.session_state["preset_metadata"] = "preset_metadata_base"
            st.session_state.form_data = {}
            # redirect
            st.switch_page("pages/4-metadata_management.py")
        except TypeError:
            st.warning("You need to select a preset")
