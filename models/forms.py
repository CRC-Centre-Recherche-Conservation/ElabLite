from dataclasses import dataclass, field
from datetime import date
from dateutil.parser import parse, ParserError
import streamlit as st
from typing import List, Union

from models.validator import validate_email, validate_url


@dataclass
class MetadataForms:
    """
        A class to represent metadata forms with various attributes.

        Attributes:
            name (str): The name of the metadata field.
            field_type (str): The type of the metadata field (e.g., 'text', 'number').
            value (Union[str, int, float]): The value of the metadata field.
            description (str, optional): A description of the metadata field. Defaults to ''.
            options (List[str], optional): A list of options for the metadata field, if applicable.
                                            Defaults to an empty list.
            required (bool, optional): Whether the metadata field is required. Defaults to False.
            position (int, optional): The position of the metadata field in a form. Defaults to -1.
            group_id (int, optional): The group ID to which the metadata field belongs. Defaults to 0.
            allow_multi_values (bool, optional): Whether multiple values are allowed for the metadata field.
                                                Defaults to False.
            unit (str, optional): The unit preselected of measurement for the metadata field, if applicable.
                                    Defaults to None.
            units (List[str], optional): A list of possible units of measurement for the metadata field.
                                        Defaults to an empty list.
    """
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
    readonly: bool = False

    def render(self, disabled):
        """
        Rendering streamlit widgets according to type detected
        :param disabled: Whether the widget should be disabled
        """

        field_label = self.name.replace('_', ' ')
        getattr(self, f"_render_{self.field_type}_field")(field_label, disabled)

    @classmethod
    def generate_form(cls, metadata, disabled: bool = False):
        """
        Iteratively generates forms based on metadata.

        This method uses the provided metadata to generate form fields within a Streamlit session.
        It ensures that session state variables for form data, required fields, and extra fields are initialized.
        It sorts the extra fields based on their position and iteratively creates and renders each form field.

        Args:
            metadata (dict): A dictionary containing metadata for the form fields. It should include an 'extra_fields' key,
                             which contains the details of each form field such as type, position, group_id, and other attributes.
            disabled (bool): False as default value. To disable widget editing

        Example:
            metadata = {
                'extra_fields': {
                    'field1': {'type': 'text', 'value': 'default1', 'position': 1, 'required': True},
                    'field2': {'type': 'number', 'value': 0, 'position': 2, 'required': False}
                }
            }
            MyClass.generate_form(metadata)
        """
        # Initialize session state variables
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {}
        if 'required_form' not in st.session_state:
            st.session_state.required_form = []
        if 'extra_fields' not in st.session_state:
            st.session_state.extra_fields = {}

        st.session_state['extra_fields'] = metadata.get('extra_fields', {})
        sorted_fields = sorted(st.session_state['extra_fields'].items(),
                               key=lambda x: x[1]['position'] if 'position' in x[1] else -1)

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

            unit = None
            if field_type == 'number':
                if isinstance(value, str) and '||' in value:
                    value, unit = value.split('||', 1)
                else:
                    # Initialize unit as None if it doesn't exist in the JSON
                    unit = field_data.get('unit', None)

            readonly = field_data.get('readonly', False)
            if not disabled:
                disabled_ = readonly
            else:
                disabled_ = disabled

            # cleaning
            field_data.pop('value', None)
            field_data.pop('type', None)
            field_data.pop('unit', None)

            # execute
            field_ = cls(field_name, field_type, value=value, unit=unit, **field_data)
            field_.render(disabled=disabled_)
            if field_.required:
                st.session_state.required_form.append(field_.value)

            if field_type == 'number' and field_.unit:
                st.session_state.form_data[field_name] = f"{field_.value}||{field_.unit}"
            else:
                st.session_state.form_data[field_name] = field_.value

    def _render_text_field(self, label: str, disabled: bool):
        """Text field rendering"""
        self.value = st.text_input(label + " *" if self.required else label,
                                   value=self.value,
                                   help=self.description,
                                   disabled=disabled)

    def _render_select_field(self, label: str, disabled: bool):
        """Select field rendering"""
        if self.allow_multi_values:
            self.value = st.multiselect(label + " *" if self.required else label, self.options,
                                        default=self.value,
                                        help=self.description,
                                        disabled=disabled)
        else:
            self.value = st.selectbox(label + " *" if self.required else label, self.options,
                                      index=self.options.index(self.value) if self.value in self.options else 0,
                                      help=self.description,
                                      disabled=disabled)

    def _render_date_field(self, label: str, disabled: bool):
        """Date field rendering"""
        try:
            date_exp = parse(str(self.value))
            self.value = st.date_input(label + " *" if self.required else label,
                                       value=date_exp,
                                       help=self.description,
                                       disabled=disabled)
        except ParserError:
            self.value = st.date_input(label + " *" if self.required else label,
                                       value=date.today(),
                                       help=self.description,
                                       disabled=disabled)

    def _render_datetime_local_field(self, label: str, disabled: bool):
        """DateTime field rendering"""
        self.value = st.date_input(label + " *" if self.required else label,
                                   value=date.today(),
                                   help=self.description,
                                   disabled=disabled)

    def _render_checkbox_field(self, label: str, disabled: bool):
        """Checkbox field rendering"""
        self.value = st.checkbox(label + " *" if self.required else label,
                                 value=self.value,
                                 help=self.description,
                                 disabled=disabled)

    def _render_email_field(self, label: str, disabled: bool):
        """Email field rendering"""
        self.value = st.text_input(label + " *" if self.required else label,
                                   value=self.value,
                                   help=self.description,
                                   on_change=validate_email,
                                   args=(self.value,),
                                   disabled=disabled)

    def _render_time_field(self, label: str, disabled: bool):
        """Time field rendering"""
        self.value = st.time_input(label + " *" if self.required else label,
                                   value=self.value,
                                   help=self.description,
                                   disabled=disabled)

    def _render_number_field(self, label: str, disabled: bool):
        """Number field rendering. In container"""
        col1, col2 = st.columns([8, 2])
        with col1:
            try:
                value = float(self.value)
            except (ValueError, TypeError):
                value = 0.0
            self.value = st.number_input(label + " *" if self.required else label,
                                         value=value,
                                         help=self.description,
                                         step=None,
                                         format="%e",
                                         disabled=disabled)

        key_found = False
        n_key = 1
        unique_key_prefix = "form_1"

        with col2:
            if self.units:
                try:
                    self.unit = st.selectbox(
                        "Unit",
                        self.units,
                        index=self.units.index(self.unit),
                        disabled=disabled
                    )
                    key_found = True
                except Exception:
                    while not key_found and n_key < 100:  # Prevent infinite loop
                        try:
                            # Continue assigning unique keys in the retry block
                            self.unit = st.selectbox(
                                "Unit",
                                self.units,
                                index=self.units.index(self.unit),
                                disabled=disabled,
                                key=f"{unique_key_prefix}_unit_select_{n_key}"  # Unique key with n_key
                            )
                            key_found = True
                        except Exception:
                            n_key += 1
                if not key_found:
                    st.warning("Failed to generate unit box (key error)")

    def _render_url_field(self, label: str, disabled: bool):
        """URL field rendering"""
        self.value = st.text_input(label + " *" if self.required else label,
                                   value=self.value,
                                   help=self.description,
                                   disabled=disabled,
                                   on_change=validate_url,
                                   args=(self.value,))

    def _render_radio_field(self, label: str, disabled: bool):
        """Radio render field"""
        self.value = st.radio(label + " *" if self.required else label,
                              value=self.value,
                              help=self.description,
                              disabled=disabled)

    def _render_items_field(self, label: str, disabled: bool):
        """Items render field"""
        try:
            value = int(self.value)
        except (ValueError, TypeError):
            value = 0
        self.value = st.number_input(label + " *" if self.required else label,
                                     value=value,
                                     help=self.description,
                                     step=1,
                                     format=None,
                                     disabled=disabled)

    def _render_users_field(self, label: str, disabled: bool):
        """Users render field"""
        try:
            value = int(self.value)
        except (ValueError, TypeError):
            value = 0
        self.value = st.number_input(label + " *" if self.required else label,
                                     value=value,
                                     help=self.description,
                                     step=1,
                                     format=None,
                                     disabled=disabled)

    def _render_experiments_field(self, label: str, disabled: bool):
        """Experiments render field"""
        try:
            value = int(self.value)
        except (ValueError, TypeError):
            value = 0
        self.value = st.number_input(label + " *" if self.required else label,
                                     value=value,
                                     help=self.description,
                                     step=1,
                                     format=None,
                                     disabled=disabled)