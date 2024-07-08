import os
from time import sleep
import streamlit as st

from utils.menu import menu
from utils.manager import manage_temp_dir

st.title("Load an experiment")
menu()
option = st.sidebar.radio("Options", ["Import save", "Load existing save"])
st.sidebar.divider()
templates_dir = manage_temp_dir(child='presets')

### OPTIONS ###
if option == "Import save":
    uploaded_file = st.file_uploader("Upload a file",
                                     type=["elablite"],
                                     accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state["selected_template"] = os.path.join(templates_dir, uploaded_file.name)
        # Save the uploaded file to the temporary directory
        with open(st.session_state["selected_template"], "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        # re init
        st.session_state['metadata_base'] = None
        st.session_state['template_metadata'] = None
        st.session_state['form_data'] = None
        # var
        st.session_state["step_metadata"] = "step_metadata_base"
        st.session_state.form_data = {}
        # redirect
        sleep(1.5)
        st.switch_page("pages/2-metadata_forms.py")
elif option == "Load existing save":
    templates = os.listdir(templates_dir)
    selected_template = st.selectbox("Select a recent preset/template", templates,
                                     index=None, placeholder="Choosing ...")
    if st.button('Validate'):
        try:
            # re init
            st.session_state['metadata_base'] = None
            st.session_state['template_metadata'] = None
            st.session_state['form_data'] = None
            # var
            st.session_state["selected_template"] = os.path.join(templates_dir, selected_template)
            st.session_state["step_metadata"] = "step_metadata_base"
            st.session_state.form_data = {}
            # redirect
            st.switch_page("pages/2-metadata_forms.py")
        except TypeError:
            st.warning("You need to select a preset")
