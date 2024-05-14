from dataclasses import dataclass, field
from datetime import date
from dateutil.parser import parse, ParserError
import streamlit as st
from typing import List, Union

class BaseForms:
    pass


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
        :return: function widget
        """
        field_label = self.name.replace('_', ' ').title()

        getattr(self, f"_render_{self.field_type}_field")(field_label)

    @classmethod
    def generate_form(cls, metadata):
        """
        Iteration generation forms
        :param metadata: dict, field parameters
        :return: rendering streamlit widgets forms
        """
        extra_fields = metadata.get('extra_fields', {})
        sorted_fields = sorted(extra_fields.items(), key=lambda x: x[1]['position'] if 'position' in x[1] else -1)
        group_id = cls.group_id
        for field_name, field_data in sorted_fields:
            field_type = field_data.get('type', 'text')
            field_group_id = field_data.get('group_id', 0)
            if group_id != field_group_id:
                group_id = field_group_id
                st.divider()
            # cleaning parameters
            field_data.pop('type', None)
            # execute
            field_ = cls(field_name, field_type, **field_data)
            field_.render()

    def _render_text_field(self, label: str):
        st.text_input(label, value=self.value, key=self.name, help=self.description)

    def _render_select_field(self, label):
        st.selectbox(label, self.options, index=self.options.index(self.value) if self.value in self.options else 0,
                     key=self.name, help=self.description)

    def _render_date_field(self, label: str):
        try:
            date_exp = parse(self.value)
            st.date_input(label, value=date_exp, key=self.name, help=self.description)
        except ParserError:
            st.date_input(label, value=date.today(), key=self.name, help=self.description)

    def _render_datetime_local_field(self, label: str):
        st.date_input(label, value=date.today(), key=self.name, help=self.description)

    def _render_checkbox_field(self, label: str):
        st.checkbox(label, value=self.value, key=self.name, help=self.description)

    def _render_email_field(self, label: str):
        st.text_input(label, value=self.value, key=self.name, help=self.description)

    def _render_time_field(self, label: str):
        st.time_input(label, value=self.value, key=self.name, help=self.description)

    def _render_number_field(self, label: str):
        col1, col2 = st.columns([8, 2])
        with col1:
            try:
                st.number_input(label, value=float(self.value), key=self.name, help=self.description, step=None, format='%g')
            except Exception:
                st.number_input(label, value=float(0), key=self.name, help=self.description, step=None, format='%g')
        with col2:
            st.selectbox("Unit", self.units, index=self.units.index(self.unit), key='unit')

    def _render_url_field(self, label: str):
        st.text_input(label, value=self.value, key=self.name, help=self.description)

    def _render_radio_field(self, label: str):
        st.radio(label, value=self.value, key=self.name, help=self.description)
