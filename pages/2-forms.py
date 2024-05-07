import streamlit as st
import os

from utils.parser import TemplatesReader

def generate_form(metadata):
    st.info(type(metadata))
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
            st.date_input(field_label, value=field_value, key=field_name, help=field_description)

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