from dataclasses import dataclass, field
from datetime import date
from dateutil.parser import parse, ParserError
import streamlit as st
from typing import List, Union

from models.validator import validate_email, validate_url

@dataclass
class MetadataForms:
    name: str
    field_type: str
    value: Union[str, int, float]
    description: str = ''
    options: List[str] = field(default_factory=list)
    required: bool = False
    position: int = -1
    group_id: int = 0
    allow_multi_values: bool = False
    unit: str = None
    units: List[str] = field(default_factory=list)

    def render(self):
        """
        Rendering streamlit widgets according to type detected
        """

        field_label = self.name.replace('_', ' ')
        getattr(self, f"_render_{self.field_type}_field")(field_label)

    @classmethod
    def generate_form(cls, metadata):
        """
        Iteration generation forms
        """
        extra_fields = metadata.get('extra_fields', {})
        sorted_fields = sorted(extra_fields.items(), key=lambda x: x[1]['position'] if 'position' in x[1] else -1)
        #var
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {}
        if 'required_form' not in st.session_state:
            st.session_state.required_form = []

        group_id = cls.group_id
        for field_name, field_data in sorted_fields:
            field_type = field_data.get('type', 'text')
            field_group_id = field_data.get('group_id', 0)
            if group_id != field_group_id:
                group_id = field_group_id
                st.divider()
            # cleaning parameters
            if bool(st.session_state.form_data):
                # get value in memory
                value = st.session_state.form_data.get(field_name, field_data['value'])
            else:
                value = field_data['value']
            field_data.pop('value', None)
            field_data.pop('type', None)
            # execute
            field_ = cls(field_name, field_type, value=value, **field_data)
            field_.render()
            if field_.required:
                st.session_state.required_form.append(field_.value)
            st.session_state.form_data[field_name] = field_.value

    def _render_text_field(self, label: str):
        self.value = st.text_input(label, value=self.value, help=self.description)

    def _render_select_field(self, label: str):
        if self.allow_multi_values:
            self.value = st.multiselect(label, self.options, default=self.value, help=self.description)
        else:
            self.value = st.selectbox(label, self.options,
                                      index=self.options.index(self.value) if self.value in self.options else 0,
                                      help=self.description)

    def _render_date_field(self, label: str):
        try:
            date_exp = parse(str(self.value))
            self.value = st.date_input(label, value=date_exp, help=self.description)
        except ParserError:
            self.value = st.date_input(label, value=date.today(), help=self.description)

    def _render_datetime_local_field(self, label: str):
        self.value = st.date_input(label, value=date.today(), help=self.description)

    def _render_checkbox_field(self, label: str):
        self.value = st.checkbox(label, value=self.value, help=self.description)

    def _render_email_field(self, label: str):
        self.value = st.text_input(label, value=self.value, help=self.description, on_change=validate_email,
                                   args=(self.value,))

    def _render_time_field(self, label: str):
        self.value = st.time_input(label, value=self.value, help=self.description)

    def _render_number_field(self, label: str):
        col1, col2 = st.columns([8, 2])
        with col1:
            try:
                self.value = st.number_input(label, value=float(self.value), help=self.description, step=None,
                                             format='%g')
            except Exception:
                self.value = st.number_input(label, value=float(0), help=self.description, step=None, format='%g')
        with col2:
            self.value = st.selectbox("Unit", self.units, index=self.units.index(self.unit))

    def _render_url_field(self, label: str):
        self.value = st.text_input(label, value=self.value, help=self.description, on_change=validate_url,
                                   args=(self.value,))

    def _render_radio_field(self, label: str):
        self.value = st.radio(label, value=self.value, help=self.description)
