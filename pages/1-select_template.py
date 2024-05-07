import os
from time import sleep
import streamlit as st

from utils.manager import manage_temp_dir


st.title("Upload or Select Template")
option = st.sidebar.radio("Options", ["Upload Template", "Select existing template"])

templates_dir = manage_temp_dir()

if option == "Upload Template":
    uploaded_file = st.file_uploader("Upload a file", type=["json", "csv", "eln"])
    if uploaded_file is not None:
        st.session_state["selected_template"] = os.path.join(templates_dir, uploaded_file.name)
        # Save the uploaded file to the temporary directory
        with open(st.session_state["selected_template"], "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success("File uploaded successfully!")
        st.sidebar.write("Go to the next page to view the template.")
        sleep(0.5)
        st.switch_page("pages/2-metadata_forms.py")
elif option == "Select existing template":
    st.write("Select a recent template:")
    templates = os.listdir(templates_dir)
    selected_template = st.selectbox("Select a template", templates)
    if selected_template:
        st.session_state["selected_template"] = os.path.join(templates_dir, selected_template)
        st.sidebar.write("Go to the next page to view the template.")
        if st.button('Validate'):
            st.switch_page("pages/2-metadata_forms.py")