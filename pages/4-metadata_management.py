import os
import pandas as pd
from pandas import Series as SeriesType
import streamlit as st
import time
from datetime import datetime
from streamlit_star_rating import st_star_rating
from streamlit_tags import st_tags

from models.forms import MetadataForms
from models.technical import TechniqueOption, TECHNIQUES
from utils.manager import generate_csv, zip_experience, files_management, convert_df
from utils.menu import menu
from utils.parser import TemplatesReader




### BASIC ###

# INIT TEMPLATE READER #
reader = TemplatesReader(st.session_state["selected_preset"])
# Get preset
metadata_base, form_data = reader.read_preset()
if metadata_base is not None and form_data is not None:
    st.session_state['metadata_base'] = metadata_base
    st.session_state['form_data'] = form_data

dataframe_metadata = reader.read_dataframe()
if dataframe_metadata is not None:
    st.session_state['dataframe_metadata'] = dataframe_metadata
del form_data, metadata_base, dataframe_metadata


def step_metadata_base():
    """Step 1 page - Base forms experience"""
    st.header("Experiment Base")
    if "metadata_base" not in st.session_state or st.session_state['metadata_base'] is None:
        st.session_state["metadata_base"] = {}

    metadata = st.session_state["metadata_base"]

    with st.container(border=True):
        title = st.text_input("Title *", help="Title of the experience", value=metadata.get("title", ""))

        # Technical box
        col1, col2 = st.columns([12, 1])

        with col1:
            technical_code = st.selectbox("Select a technique *", options=TECHNIQUES.keys(),
                                          format_func=lambda x: TECHNIQUES[x].english_name,
                                          index=list(TECHNIQUES.keys()).index(metadata["technical"].code)
                                          if metadata.get("technical") else None)
            technical = TECHNIQUES.get(technical_code)
        with col2:
            with st.container(height=11, border=False):  # css cheat button
                st.empty()
            with st.container():
                add_button = st.button(":heavy_plus_sign:", help="Add a new technique")
        if add_button:
            TechniqueOption.open_add_technique_modal()

        date = st.date_input("Date *", value=metadata.get("date", datetime.now()))
        author = st.text_input("Author *", value=metadata.get("author"))
        commentary = st.text_area("Commentary", value=metadata.get("commentary"))
        tags = st_tags(label="tags", maxtags=8, value=metadata.get("tags", []))
        st.divider()
        rating = st_star_rating(label="Rate your experiment", maxValue=5, defaultValue=metadata.get("rating", 0))

        submit_enabled = all((title, date, author, technical_code))
        st.session_state["submit_enabled"] = submit_enabled
        st.session_state["metadata_base"] = {"title": title, "date": date, "author": author, "commentary": commentary,
                                             'tags': tags, 'rating': rating, 'technical': technical}


### METADATA INSTRUMENTAL ###

def step_metadata_forms():
    """Step 2 page - Metadata forms instrumental"""
    if "template_metadata" not in st.session_state:
        st.session_state["template_metadata"] = None
    st.header("Experiment Metadata Preset")
    try:
        st.session_state['template_metadata'] = reader.read_metadata()
        with st.expander("General metadata preset"):
            st.session_state.required_form = []
            MetadataForms.generate_form(st.session_state['template_metadata'], disabled=True)
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

    df = st.session_state['dataframe_metadata']

    def find_filename(row):
        """check and get filename corresponding to row"""
        for filename in filenames:
            if row['IdentifierAnalysis'] in filename and row['Object/Sample'] in filename:
                return filename
        return ''

    df['Filename'] = df.apply(find_filename, axis=1)
    # Filename first
    df = df[['Filename'] + [col for col in df.columns if col != 'Filename']]

    st.session_state["dataframe_metadata_edited"] = st.data_editor(df)


def step_metadata_files():
    """Step 3 page - Manage metadata with datafiles files"""
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = {}

    st.session_state["submit_enabled"] = True

    st.header("Files Mapping Editor")
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

    code = st.session_state['metadata_base']['technical'].code
    date = st.session_state['metadata_base']['date'].strftime('%Y%m%d')
    new_filename = str(date) + "_" + code + "_" + "_".join(filename_parts) + extension
    return new_filename.replace("__", "_")


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
    if "filename_validated" not in st.session_state:
        st.session_state["filename_validated"] = False

    st.header("Download Experiments")
    st.subheader("Preparing ...")
    df = st.session_state["dataframe_metadata_edited"]
    # Generate alternative titles non-bundled
    df['new_title'] = df.apply(lambda x: generate_newtitle(x, st.session_state['metadata_base']['title']), axis=1)

    exclude_columns = ['Filename', 'new_title', 'new_Filename']
    selected_columns = st.multiselect("Select columns to include in filename (in order)",
                                      [col for col in df.columns.tolist() if col not in exclude_columns])

    col1, col2, col3 = st.columns([1, 4, 7])
    with col2:
        if st.button("Validation filename"):
            try:
                df['new_Filename'] = df.apply(lambda x: generate_filename(x, selected_columns), axis=1)
                st.toast("Success!", icon='🎉')
                st.session_state["filename_validated"] = True
                with col3:
                    alert = st.caption(f"Example: {df['new_Filename'].iloc[0]}")
                    time.sleep(2)
                    alert.empty()
            except Exception as err:
                st.toast("Failed", icon='🚨')
                st.info(err)
    with col1:
        st.checkbox("Filename validated", value=st.session_state["filename_validated"], disabled=True)


    with st.container():
        st.subheader("Download ...")

        st.markdown("""
        By checking the toggle, you can group all the files within a single experiment in the electronic laboratory 
        notebook. On the other hand, if files and its metadata are to be considered separately,
         the toggle should be unchecked.
        """)
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
                zip_buffer = zip_experience(csv_, uploaded_files_, logs_process=convert_df(df))
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
    st.info(f"""You are using the template `{st.session_state["selected_preset"]}`""")
    current_step = st.session_state["preset_metadata"]
    st.session_state["submit_enabled"] = False
    if current_step == "preset_metadata_base":
        step_metadata_base()
    elif current_step == "preset_metadata_forms":
        step_metadata_forms()
    elif current_step == "preset_metadata_files":
        step_metadata_files()
    elif current_step == "preset_metadata_download":
        step_metadata_download()


def next_step():
    """
    Moves to the next step in the metadata page.
    """
    if st.session_state["preset_metadata"] == "preset_metadata_base":
        st.session_state["preset_metadata"] = "preset_metadata_forms"
    elif st.session_state["preset_metadata"] == "preset_metadata_forms":
        st.session_state["preset_metadata"] = "preset_metadata_files"
    elif st.session_state["preset_metadata"] == "preset_metadata_files":
        st.session_state["preset_metadata"] = "preset_metadata_download"


def previous_step():
    """
    Moves to the previous step in the metadata page.
    """
    if st.session_state["preset_metadata"] == "preset_metadata_forms":
        st.session_state["preset_metadata"] = "preset_metadata_base"
    elif st.session_state["preset_metadata"] == "preset_metadata_files":
        st.session_state["preset_metadata"] = "preset_metadata_forms"
    elif st.session_state["preset_metadata"] == "preset_metadata_download":
        st.session_state["preset_metadata"] = "preset_metadata_files"


### PAGE ###

st.title("Metadata & Files Management")
menu()

# check templates
if "selected_preset" in st.session_state and os.path.exists(st.session_state["selected_preset"]):

    # display page form
    display_forms()

    # buttons navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["preset_metadata"] != "preset_metadata_base":
            if st.button("⏮️ Previous", on_click=previous_step):
                pass
    with col2:
        if st.session_state["preset_metadata"] != "preset_metadata_download":
            if st.button("Next ⏭️", on_click=next_step, disabled=not st.session_state["submit_enabled"]):
                pass
        elif st.session_state["preset_metadata"] == "preset_metadata_forms":
            if st.button("Next ⏭️", on_click=next_step,
                         disabled=not (st.session_state["submit_enabled"] and st.session_state["validation_error"])):
                pass

# redirection empty templates
else:
    st.warning("Please select or upload a preset/template metadata")
    with st.spinner('Redirection'):
        time.sleep(3)
    st.switch_page("pages/3-metadata_preset.py")
