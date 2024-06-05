import os
import pandas as pd
import streamlit as st
import time
from datetime import datetime
from streamlit_star_rating import st_star_rating
from streamlit_tags import st_tags

from models.forms import MetadataForms
from utils.manager import generate_csv, zip_experience
from utils.menu import menu
from utils.parser import TemplatesReader


### BASIC ###

def step_metadata_base():
    if "metadata_base" not in st.session_state:
        st.session_state["metadata_base"] = None
    st.header("Experience presentation")
    with st.container(border=True):
        title = st.text_input("Title", help="Title of the experience")
        date = st.date_input("Date", value=datetime.now())
        author = st.text_input("Author")
        commentary = st.text_area("Commentary")
        tags = st_tags(label="tags", maxtags=8)
        rating = st_star_rating(label="Rate you experience", maxValue=5, defaultValue=0)
        submit_enabled = all((title, date, author))
        st.session_state["submit_enabled"] = submit_enabled
        st.session_state["metadata_base"] = {"title": title, "date": date, "author": author, "commentary": commentary, 'tags': tags, 'rating': rating}


### METADATA INSTRUMENTAL ###

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


### EDITING DATAFRAME FILE ###

def display_file_metadata(filenames: list):
    if "dataframe_metadata" not in st.session_state:
        st.session_state["dataframe_metadata"] = None

    form_data = st.session_state.form_data
    df = pd.DataFrame([{'Filename': filenames[0]} | form_data], columns=['Filename', *form_data.keys()])
    for filename in filenames[1:]:
        row_data = {'Filename': filename} | form_data
        df = pd.concat([df, pd.DataFrame([row_data], columns=['Filename', *form_data.keys()])], ignore_index=True)

    df['IdentifierAnalysis'] = ""
    df['Object'] = ""
    #ordering
    columns_order = ['Filename', 'IdentifierAnalysis', 'Object', *form_data.keys()]
    df = df[columns_order]

    st.session_state["dataframe_metadata"] = st.data_editor(df)


def step_metadata_files():
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    st.session_state["submit_enabled"] = True

    st.header("Files metadata editor")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, key='upload_files')

    if uploaded_files:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.session_state['uploaded_files'].append({
                'name': uploaded_file.name,
                'data': bytes_data
            })

    with st.spinner("Processing dataframe..."):
        while not uploaded_files:
            time.sleep(1)
        file_names = [file.name for file in uploaded_files]
    if file_names is not None:
        st.subheader("Uploaded File Names")
        display_file_metadata(file_names)


### DOWNLOAD PAGE ###

def generate_filename(row, selected_columns):
    filename_parts = []
    for col in selected_columns:
        filename_parts.append(str(row[col]))

    date = st.session_state['metadata_base']['date'].strftime('%Y%m%d')
    return str(date) + "_" + "_".join(filename_parts)

def step_metadata_download():

    if "grouped_exp" not in st.session_state:
        st.session_state["grouped_exp"] = False

    st.header("Download experiences")
    st.subheader("Preparing ...")
    df = st.session_state["dataframe_metadata"]
    selected_columns = st.multiselect("Select columns to include in filename", df.columns.tolist())

    disabled = True

    if st.button("Generate Filename"):
        df['new_Filename'] = ''
        for index, row in df.iterrows():
            filename = generate_filename(row, selected_columns)
            df['new_Filename'] = filename
        alert = st.toast("Success!", icon='🎉')
        time.sleep(2)
        alert.empty()

    st.subheader("Download ...")

    grouped = st.toggle('Grouping analysis ?', help='Activate to group all analyses in one experience')

    if grouped:
        st.session_state["grouped_exp"] = True
    else:
        st.session_state["grouped_exp"] = False

    # st.info(st.session_state['metadata_base'])
    # st.info(type(df))

    if st.button("Generate files", type='primary'):
        with st.status("Generating data...") as status:
            st.write("Generating CSV...")
            csv_ = generate_csv(base_mtda=st.session_state['metadata_base'],
                         exp_mtda=df,
                         grouped=st.session_state["grouped_exp"])
            time.sleep(2)
            st.write("Renaming files...")
            time.sleep(1)
            st.write("Zipping...")
            zip_buffer = zip_experience(csv_)
            time.sleep(2)
            status.update(label="Process complete!", state="complete", expanded=False)
            disabled=False

        st.download_button(
            label="Download Zip",
            data=zip_buffer.getvalue(),
            file_name=f"{datetime.today().strftime('%Y%m%d')}_experiences.zip",
            mime="application/zip",
            disabled=disabled
        )



### INTERN PAGE MANAGEMENT ###

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
            if st.button("Next ⏭️", on_click=next_step,
                         disabled=not (st.session_state["submit_enabled"] and st.session_state["validation_error"])):
                pass

# redirection empty templates
else:
    st.warning("Please select/upload a template on the first page.")
    with st.spinner('Redirection'):
        time.sleep(3)
    st.switch_page("pages/1-select_template.py")
