import copy
import os
import pandas as pd
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

try:
    reader = TemplatesReader(st.session_state["selected_template"])
except KeyError:
    # Go to home if reload page or anything which delete selected_template session
    st.switch_page("app.py")

if not st.session_state['basic_executed']:
    # Get preset
    metadata_base, form_data = reader.read_preset()
    if metadata_base is not None and form_data is not None:
        st.session_state['metadata_base'] = metadata_base
        st.session_state['form_data'] = form_data

    dataframe_metadata = reader.read_dataframe()
    if dataframe_metadata is not None:
        st.session_state['dataframe_metadata'] = dataframe_metadata
    del form_data, metadata_base, dataframe_metadata

    # Set the flag to True after execution
    st.session_state['basic_executed'] = True


def step_metadata_base():
    """Step 1 page - Base forms experience"""
    st.header("Experiment Base")

    metadata = st.session_state["metadata_base"]

    with st.container(border=True):
        # Config Project
        with st.popover("⚙️  Project Config"):
            st.markdown("Describe the project")
            project_longname = st.text_input("Project (longname)", value=metadata.get("project_longname"))
            project_shortname = st.text_input("Project (shortname)", value=metadata.get("project_shortname"))
            project_uri = st.text_input("Project (URI)", value=metadata.get("project_uri"),
                                        help="URL of the project")

        title = st.text_input("Title *", help="Title of the experiment", value=metadata.get("title"))

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
                                             'tags': tags, 'rating': rating, 'technical': technical,
                                             'project_longname': project_longname,
                                             'project_shortname': project_shortname, "project_uri": project_uri}


### METADATA INSTRUMENTAL ###

def step_metadata_forms():
    """Step 2 page - Metadata forms instrumental"""
    if "template_metadata" not in st.session_state:
        st.session_state["template_metadata"] = None
    st.header("Experience Metadata")
    original_metadata = reader.read_metadata()
    working_metadata = copy.deepcopy(original_metadata)
    try:
        st.session_state['template_metadata'] = original_metadata
        with st.container():
            st.session_state.required_form = []
            MetadataForms.generate_form(working_metadata)
            st.session_state["submit_enabled"] = all(st.session_state.required_form)
    except Exception as e:
        st.error(f"Error: {e}")
    # Re init without modification MetadataForms.generate_form()
    # To save the good template in .elablite
    st.session_state['template_metadata'] = original_metadata


### EDITING DATAFRAME FILE ###

def add_row(edited_df: pd.DataFrame):
    """
    Adds a new row to the DataFrame stored in the Streamlit. Return edited df to session state 'dataframe_metadata'
    :param edited_df: DataFrame storing the data
    """
    df = edited_df
    form_data = st.session_state.form_data

    new_row = pd.DataFrame([form_data], columns=[*form_data.keys()])
    new_row['IdentifierAnalysis'] = None
    new_row['Object/Sample'] = None
    new_row['LocalisationAnalysis'] = None
    st.session_state.dataframe_metadata = pd.concat([df, new_row], ignore_index=True)


def step_metadata_files():
    """Step 3 page - Manage metadata with datafiles files"""
    st.session_state["submit_enabled"] = True

    st.header("Files Metadata Editor")
    with st.expander("Help", expanded=False):
        st.markdown("""
    This spreadsheet is quickly made up of metadata based on your analyses. Two columns are essential to the analysis: 
- `IdentifierAnalysis` : corresponds to the identifier of your analysis, both internal and external (e.g. *XRF0001*).
- `Object/Sample` : corresponds to the identifier of your study object or sample (e.g. *AvranchesMs59f01v*, 
*MNHN-X314z8j*, etc. ....). Your text must be made without spaces, either by separating with a capital letter or with a 
hyphen (-) to show continuity. The underscore is used to separate parameters in the file name.
- `LocalisationAnalysis` : description area to help locate and differentiate the analysis. If you later wish to keep 
this parameter within the file name, it must not contain spaces or be too descriptive (e.g. *RedTopEnlighment*).
        
In this spreadsheet you can add cells (with the `+` button), delete cells or enlarge cells. If you wish to add a new
cell and apply metadata. Ideally, select the first row and drag. Alternatively, you can copy/paste the line.

Use the `Add row` button to add a new row pre-filled with the experimental metadata defined in the previous step. 
If you wish, you can return to the previous page to edit your template and add rows with updated metadata.
    """)

    if "dataframe_metadata" not in st.session_state:
        st.session_state["dataframe_metadata"] = None

    form_data = st.session_state.form_data

    if st.session_state['dataframe_metadata'] is not None:
        df = st.session_state['dataframe_metadata'].copy()
    else:
        df = pd.DataFrame([form_data], columns=[*form_data.keys()])
        # New column
        df['IdentifierAnalysis'] = None
        df['Object/Sample'] = None
        df['LocalisationAnalysis'] = None
        # ordering
        columns_order = ['IdentifierAnalysis', 'Object/Sample', 'LocalisationAnalysis', *form_data.keys()]
        df = df[columns_order]
        st.session_state.dataframe_metadata = df

    edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True)

    # State saving
    st.session_state['has_changes'] = st.session_state["dataframe_metadata"].equals(edited_df)

    col4, col1, col2, col3 = st.columns([3, 1, 1, 9])
    with col2:
        if st.button("Add row", on_click=add_row, args=(edited_df,), help="Add a row with experimental parameters"):
            st.session_state["dataframe_metadata"] = edited_df
    with col1:
        if st.button("Save", type="primary", disabled=st.session_state['has_changes']):
            st.session_state["dataframe_metadata"] = edited_df
            st.toast("Changes saved successfully!", icon="✅")
            st.rerun()


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
                             template_metadata=st.session_state["template_metadata"],
                             dataframe_metadata=st.session_state["dataframe_metadata"]),
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
    elif st.session_state["step_metadata"] == "step_metadata_download":
        st.session_state["step_metadata"] = "step_metadata_files"
    elif st.session_state["step_metadata"] == "step_metadata_files":
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
