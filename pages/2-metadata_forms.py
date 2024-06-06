import os
import pandas as pd
from pandas import Series as SeriesType
import streamlit as st
import time
from datetime import datetime
from streamlit_star_rating import st_star_rating
from streamlit_tags import st_tags

from models.forms import MetadataForms
from utils.manager import generate_csv, zip_experience, files_management
from utils.menu import menu
from utils.parser import TemplatesReader


### BASIC ###

def step_metadata_base():
    """Step 1 page - Base forms experience"""
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
        st.session_state["metadata_base"] = {"title": title, "date": date, "author": author, "commentary": commentary,
                                             'tags': tags, 'rating': rating}


### METADATA INSTRUMENTAL ###

def step_metadata_forms():
    """Step 2 page - Metadata forms instrumental"""
    if "template_metadata" not in st.session_state:
        st.session_state["template_metadata"] = None
    st.header("Experience presentation")
    reader = TemplatesReader(st.session_state["selected_template"])
    try:
        st.session_state['template_metadata'] = reader.read_metadata()
        with st.container():
            st.session_state.required_form = []
            MetadataForms.generate_form(st.session_state['template_metadata'])
            st.session_state["submit_enabled"] = all(st.session_state.required_form)
    except Exception as e:
        st.error(f"Error: {e}")


### EDITING DATAFRAME FILE ###

def display_file_metadata(filenames: list):
    """
        Displays metadata for a list of filenames in a Streamlit data editor.

        Parameters:
        filenames (list): A list of filenames for which metadata is to be displayed.

        Returns:
        None
    """
    if "dataframe_metadata" not in st.session_state:
        st.session_state["dataframe_metadata"] = None

    form_data = st.session_state.form_data
    df = pd.DataFrame([{'Filename': filenames[0]} | form_data], columns=['Filename', *form_data.keys()])
    for filename in filenames[1:]:
        row_data = {'Filename': filename} | form_data
        df = pd.concat([df, pd.DataFrame([row_data], columns=['Filename', *form_data.keys()])], ignore_index=True)

    df['IdentifierAnalysis'] = ""
    df['Object/Sample'] = ""
    #ordering
    columns_order = ['Filename', 'IdentifierAnalysis', 'Object/Sample', *form_data.keys()]
    df = df[columns_order]

    st.session_state["dataframe_metadata"] = st.data_editor(df)


def step_metadata_files():
    """Step 3 page - Manage metadata with datafiles files"""
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = {}

    st.session_state["submit_enabled"] = True

    st.header("Files metadata editor")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, key='upload_files')

    if uploaded_files:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.session_state['uploaded_files'][uploaded_file.name] = bytes_data

    with st.spinner("Processing dataframe..."):
        while not uploaded_files:
            time.sleep(1)
        file_names = [file.name for file in uploaded_files]
    if file_names is not None:
        st.subheader("Uploaded File Names")
        display_file_metadata(file_names)


### DOWNLOAD PAGE ###

def generate_filename(row: SeriesType, selected_columns: list) -> str:
    """
        Generates a filename based on selected columns from a DataFrame row and adds a date prefix.

        Parameters:
        row (pandas.Series): A row of data from a DataFrame.
        selected_columns (list): A list of column names to be included in the filename.

        Returns:
        str: The generated filename.
    """
    filename_parts = []
    for col in selected_columns:
        filename_parts.append(str(row[col]))

    _, extension = os.path.splitext(row['Filename'])

    date = st.session_state['metadata_base']['date'].strftime('%Y%m%d')
    return str(date) + "_" + "_".join(filename_parts) + extension


def generate_newtitle(row: SeriesType, title: str) -> str:
    """
    Generates a new title based on conditions.

    Parameters:
    row (pandas.Series): A row of data from the DataFrame.
    title (str): The base title used for generating new titles.

    Returns:
    str: A new title generated based on conditions.
    """
    if pd.notnull(row['IdentifierAnalysis']) or pd.notnull(row['Object/Sample']):
        return f"{title} -- {row['IdentifierAnalysis']}_{row['Object/Sample']}"
    else:
        return f"{title} -- {row.idx}"


def step_metadata_download():
    """Step 4 page - Generate new filenameDownload metadata"""
    if "grouped_exp" not in st.session_state:
        st.session_state["grouped_exp"] = False

    st.header("Download experiences")
    st.subheader("Preparing ...")
    df = st.session_state["dataframe_metadata"]
    df['new_title'] = df.apply(lambda x: generate_newtitle(x, st.session_state['metadata_base']['title']), axis=1) # Generate alternative titles non-bundled

    exclude_columns = ['Filename', 'new_title', 'new_Filename']
    selected_columns = st.multiselect("Select columns to include in filename (in order)", [col for col in df.columns.tolist() if col not in exclude_columns])

    col1, col2 = st.columns([4, 7])
    with col1:
        if st.button("Validation filename"):
            df['new_Filename'] = df.apply(lambda x: generate_filename(x, selected_columns), axis=1)
            st.toast("Success!", icon='🎉')
            with col2:
                alert = st.caption(f"Example: {df['new_Filename'].iloc[0]}")
            time.sleep(2)
            alert.empty()

    with st.container():
        st.subheader("Download ...")

        st.session_state["grouped_exp"] = st.toggle('Grouping analysis ?',
                                                    help='Activate to group all analyses in one experience')

        if st.button("Generate files", type='primary'):
            with st.status("Generating data...") as status:
                st.write("Generating CSV...")
                csv_ = generate_csv(base_mtda=st.session_state['metadata_base'],
                                    df_mtda=df,
                                    grouped=st.session_state["grouped_exp"])
                time.sleep(2)
                st.write("Renaming files...")
                uploaded_files_ = files_management(uploaded_files=st.session_state["uploaded_files"],
                                                   df_mtda=df,
                                                   grouped=st.session_state["grouped_exp"])
                time.sleep(1)
                st.write("Zipping...")
                zip_buffer = zip_experience(csv_, uploaded_files_)
                del uploaded_files_, csv_
                time.sleep(2)
                status.update(label="Process complete!", state="complete", expanded=False)
                st.session_state["submit_enabled"] = False

            st.download_button(
                label="Download Zip",
                data=zip_buffer.getvalue(),
                file_name=f"{datetime.today().strftime('%Y%m%d')}_experiences.zip",
                mime="application/zip",
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
    elif current_step == "step_metadata_files":
        step_metadata_files()
    elif current_step == "step_metadata_download":
        step_metadata_download()


def next_step():
    """
    Moves to the next step in the metadata page.
    """
    if st.session_state["step_metadata"] == "step_metadata_base":
        st.session_state["step_metadata"] = "step_metadata_forms"
    elif st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_files"
    elif st.session_state["step_metadata"] == "step_metadata_files":
        st.session_state["step_metadata"] = "step_metadata_download"


def previous_step():
    """
    Moves to the previous step in the metadata page.
    """
    if st.session_state["step_metadata"] == "step_metadata_forms":
        st.session_state["step_metadata"] = "step_metadata_base"
    elif st.session_state["step_metadata"] == "step_metadata_files":
        st.session_state["step_metadata"] = "step_metadata_forms"
    elif st.session_state["step_metadata"] == "step_metadata_download":
        st.session_state["step_metadata"] = "step_metadata_files"


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
