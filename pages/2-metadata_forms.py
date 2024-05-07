from datetime import date
import os
import streamlit as st

from utils.parser import TemplatesReader

def generate_form(metadata):
    #https://docs.streamlit.io/develop/api-reference/widgets -> do all fields for elab (https://doc.elabftw.net/metadata.html)
    # check required option
    # how to add unit for number
    # add regex check for input (url, email)
    extra_fields = metadata.get('extra_fields', {})
    for field_name, field_data in extra_fields.items():
        field_type = field_data.get('type')
        field_label = field_name.replace('_', ' ').title()
        field_value = field_data.get('value', '')
        field_required = field_data.get('required', False)
        field_description = field_data.get('description', '')

        if field_type == 'text':
            st.text_input(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'select':
            options = field_data.get('options', [])
            st.selectbox(field_label, options, index=options.index(field_value) if field_value in options else 0, key=field_name, help=field_description)
        elif field_type == 'date':
            st.date_input(field_label, value=False, key=field_name, help=field_description)
        elif field_type == 'datetime-local':
            st.date_input(field_label, value=date.today(), key=field_name, help=field_description)
        elif field_type == 'checkbox':
            st.checkbox(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'email':
            st.text_input(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'time':
            st.time_input(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'number':
            # https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
            st.number_input(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'url':
            st.text_input(field_label, value=field_value, key=field_name, help=field_description)
        elif field_type == 'radio':
            st.radio(field_label, value=field_value, key=field_name, help=field_description)
        else:
            raise st.error(f"Error form generation for {field_name, field_data}")

# One template with st.text_area
# and all parameters
# add button step to step metadata 'presentation, metadata, download' (erdirect page) with progress bar ?

st.title("View Template")
if "selected_template" in st.session_state and os.path.exists(st.session_state["selected_template"]):
    reader = TemplatesReader(st.session_state["selected_template"])
    st.info(reader)
    st.info(f"""You are using the template `{st.session_state["selected_template"]}`""")

    try:
        template_metadata = reader.read_metadata()
        generate_form(template_metadata)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please select/upload a template on the first page.")