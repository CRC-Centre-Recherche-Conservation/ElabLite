import streamlit as st
from typing import Dict
import pandas as pd
from datetime import datetime
from utils.manager import auto_save_experiment, get_current_save_path, set_current_save_path, create_elablite


class SaveManager:
    """
    Manage save operations for experiments with Save and Save As functionality
    """

    @staticmethod
    def get_current_save_path() -> str:
        """Get the current save path from session state"""
        return get_current_save_path()

    @staticmethod
    def initialize_save_indicator():
        """
        Initialize save indicator system
        Call this at the start of each page
        """
        if 'last_save_time' not in st.session_state:
            st.session_state['last_save_time'] = None

    @staticmethod
    def render_save_indicator():
        """
        Render save status indicator
        Shows last save time
        """
        SaveManager.initialize_save_indicator()

        last_save = st.session_state.get('last_save_time')

        if last_save:
            time_ago = (datetime.now() - last_save).total_seconds()
            if time_ago < 60:
                st.caption(f"💾 Last saved {int(time_ago)}s ago")
            elif time_ago < 3600:
                st.caption(f"💾 Last saved {int(time_ago / 60)}m ago")
            else:
                st.caption(f"💾 Last saved {int(time_ago / 3600)}h ago")
        else:
            current_path = get_current_save_path()
            if current_path:
                st.caption("💾 Ready to save")
            else:
                st.caption("⚠️ No save file yet")

    @staticmethod
    def perform_save_current() -> bool:
        """
        Perform save on the current file path (manual save)

        Returns:
            bool: True if save was successful
        """
        current_path = get_current_save_path()
        if not current_path:
            return False

        result = SaveManager._perform_save(current_path)
        if result:
            # Update save timestamp
            st.session_state['last_save_time'] = datetime.now()
        return result

    @staticmethod
    def render_save_buttons():
        """
        Render Save and Save As buttons with appropriate logic
        Returns True if save operation was performed
        """
        col1, col2, col3 = st.columns([2, 2, 6])

        save_performed = False
        current_path = get_current_save_path()

        with col1:
            # Save button - disabled if no current save path
            save_disabled = current_path is None
            if st.button("💾 Save", disabled=save_disabled,
                         help="Save to current file" if not save_disabled else "No file selected. Use Save As"):
                if SaveManager._perform_save(current_path):
                    st.toast("✅ Saved successfully!", icon="✅")
                    st.session_state['last_save_time'] = datetime.now()
                    save_performed = True
                else:
                    st.toast("❌ Save failed", icon="❌")

        with col2:
            if st.button("💾 Save As", help="Save as new file"):
                SaveManager.show_save_as_dialog()

        # Display current save file if exists
        if current_path:
            import os
            filename = os.path.basename(current_path)
            with col3:
                st.caption(f"📁 Current file: `{filename}`")

        return save_performed

    @staticmethod
    def _validate_save_data() -> tuple[bool, str]:
        """
        Validate that all required data for save is present

        Returns:
            tuple: (is_valid, error_message)
        """
        # Check metadata_base
        metadata_base = st.session_state.get('metadata_base', None)
        if not metadata_base:
            return False, "Missing metadata_base"

        # Check required fields in metadata_base
        required_fields = ['title', 'date', 'author']
        for field in required_fields:
            if not metadata_base.get(field):
                return False, f"Missing required field: {field}"

        # Check technical field
        if not metadata_base.get('technical'):
            return False, "Missing technical field"

        # Check template_metadata - Initialize if missing
        if 'template_metadata' not in st.session_state:
            try:
                from utils.parser import TemplatesReader
                if 'selected_template' in st.session_state:
                    reader = TemplatesReader(st.session_state["selected_template"])
                    st.session_state['template_metadata'] = reader.read_metadata()
                else:
                    st.session_state['template_metadata'] = {'extra_fields': {}}
            except Exception:
                st.session_state['template_metadata'] = {'extra_fields': {}}

        # form_data can be empty initially
        if 'form_data' not in st.session_state:
            st.session_state['form_data'] = {}

        # dataframe_metadata can be None
        if 'dataframe_metadata' not in st.session_state:
            st.session_state['dataframe_metadata'] = None

        return True, ""

    @staticmethod
    def _perform_save(filepath: str = None) -> bool:
        """
        Perform the actual save operation with validation

        Args:
            filepath: Path to save to. If None, will auto-generate

        Returns:
            bool: True if save was successful
        """
        try:
            # VALIDATE DATA FIRST
            is_valid, error_msg = SaveManager._validate_save_data()
            if not is_valid:
                return False

            # Collect all necessary data from session state
            metadata_base = st.session_state.get('metadata_base', {})
            form_data = st.session_state.get('form_data', {})
            template_metadata = st.session_state.get('template_metadata', {})
            dataframe_metadata = st.session_state.get('dataframe_metadata', None)

            # Perform save
            if filepath is None:
                # Auto-generate filename
                saved_path = auto_save_experiment(
                    metadata_base=metadata_base,
                    form_data=form_data,
                    template_metadata=template_metadata,
                    dataframe_metadata=dataframe_metadata
                )
            else:
                # Save to specific path
                import os
                filename = os.path.basename(filepath)
                saved_path = auto_save_experiment(
                    metadata_base=metadata_base,
                    form_data=form_data,
                    template_metadata=template_metadata,
                    dataframe_metadata=dataframe_metadata,
                    filename=filename
                )

            # Update session state with current save path
            set_current_save_path(saved_path)
            return True

        except Exception as e:
            return False

    @staticmethod
    @st.dialog("Save As")
    def show_save_as_dialog():
        """
        Show dialog for Save As operation with validation
        Can be called from any step
        """
        st.markdown("### Save experiment as...")

        # VALIDATE DATA BEFORE SHOWING DIALOG
        is_valid, error_msg = SaveManager._validate_save_data()

        if not is_valid:
            st.error(f"⚠️ Missing required data for save")
            st.error(f"**Problem:** {error_msg}")
            st.markdown("---")
            st.info("**Required data:**")
            st.markdown("""
            - ✓ Title (filled)
            - ✓ Date (selected)
            - ✓ Author (filled)
            - ✓ Technique (selected)
            """)

            if st.button("Close", use_container_width=True):
                st.rerun()
            return

        # Get suggested filename from metadata
        metadata_base = st.session_state.get('metadata_base', {})
        title = metadata_base.get('title', 'experiment')
        suggested_name = title.replace(' ', '_')[:50]

        filename = st.text_input(
            "Filename",
            value=suggested_name,
            help="Enter filename without extension (.elablite will be added automatically)"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Save", type="primary", use_container_width=True):
                if not filename.strip():
                    st.error("Please enter a filename")
                else:
                    # Try to save
                    if SaveManager._perform_save(f"{filename}.elablite"):
                        st.success(f"✅ Saved as: {filename}.elablite")
                        st.session_state['save_as_complete'] = True
                        st.session_state['last_save_time'] = datetime.now()
                        # Wait a bit before rerun to show success message
                        import time
                        time.sleep(1)
                        st.rerun()

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()

    @staticmethod
    def render_download_section():
        """
        Render download section for manual file export
        """
        st.markdown("""
        Download a copy of your experiment file to your computer for:
        - **Archiving** - Keep a permanent backup
        - **Sharing** - Send to collaborators
        - **External storage** - Save on USB, cloud, etc.
        """)

        # Validate data before allowing download
        is_valid, error_msg = SaveManager._validate_save_data()

        if not is_valid:
            st.warning(f"⚠️ Cannot download: {error_msg}")
            st.info("Please fill all required fields in Step 1 before downloading.")
            return

        metadata_base = st.session_state.get('metadata_base', {})
        form_data = st.session_state.get('form_data', {})
        template_metadata = st.session_state.get('template_metadata', {})
        dataframe_metadata = st.session_state.get('dataframe_metadata', None)

        # Generate filename suggestion
        title = metadata_base.get('title', 'experiment')
        suggested_name = title.replace(' ', '_')[:50]

        col1, col2 = st.columns([3, 7])

        with col1:
            filename = st.text_input(
                "Export filename",
                value=suggested_name,
                help='Enter the filename for export. Extension will be added automatically.',
                label_visibility="collapsed",
                placeholder="Enter filename..."
            )

        with col2:
            if not filename.strip():
                download_disabled = True
            else:
                download_disabled = False

            try:
                elablite_data = create_elablite(
                    metadata_base=metadata_base,
                    form_data=form_data,
                    template_metadata=template_metadata,
                    dataframe_metadata=dataframe_metadata
                )

                st.download_button(
                    label="📥 Download .elablite",
                    data=elablite_data,
                    file_name=f"{filename}.elablite",
                    mime="application/octet-stream",
                    disabled=download_disabled,
                    help="Download experiment file to your computer",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error creating download: {str(e)}")

        if not download_disabled:
            st.caption(f"💡 File will be saved as: `{filename}.elablite`")