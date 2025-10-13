import streamlit as st
from typing import Dict
import pandas as pd
from utils.manager import auto_save_experiment, get_current_save_path, set_current_save_path, create_elablite


class SaveManager:
    """
    Manage save operations for experiments with Save and Save As functionality
    """

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
                    save_performed = True
                else:
                    st.toast("❌ Save failed", icon="❌")

        with col2:
            if st.button("💾 Save As", help="Save as new file"):
                SaveManager._show_save_as_dialog()

        # Display current save file if exists
        if current_path:
            import os
            filename = os.path.basename(current_path)
            with col3:
                st.caption(f"📁 Current file: `{filename}`")

        return save_performed

    @staticmethod
    def _perform_save(filepath: str = None) -> bool:
        """
        Perform the actual save operation

        Args:
            filepath: Path to save to. If None, will auto-generate

        Returns:
            bool: True if save was successful
        """
        try:
            # Collect all necessary data from session state
            metadata_base = st.session_state.get('metadata_base', {})
            form_data = st.session_state.get('form_data', {})
            template_metadata = st.session_state.get('template_metadata', {})
            dataframe_metadata = st.session_state.get('dataframe_metadata', None)

            # Validate we have required data
            if not metadata_base or not template_metadata:
                st.error("Missing required data for save")
                return False

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
            st.error(f"Error during save: {str(e)}")
            return False

    @staticmethod
    @st.dialog("Save As")
    def _show_save_as_dialog():
        """
        Show dialog for Save As operation
        """
        st.markdown("### Save experiment as...")

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
                    if SaveManager._perform_save(f"{filename}.elablite"):
                        st.success(f"✅ Saved as: {filename}.elablite")
                        st.session_state['save_as_complete'] = True
                        st.rerun()
                    else:
                        st.error("Failed to save file")

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()

    @staticmethod
    def auto_save_on_change():
        """
        Perform auto-save when data changes
        Should be called in callbacks
        """
        # Only auto-save if we have a current save path
        current_path = get_current_save_path()
        if current_path:
            SaveManager._perform_save(current_path)

    @staticmethod
    def render_download_section():
        """
        Render download section for manual file export
        """
        st.subheader("📥 Export Experiment")

        metadata_base = st.session_state.get('metadata_base', {})
        form_data = st.session_state.get('form_data', {})
        template_metadata = st.session_state.get('template_metadata', {})
        dataframe_metadata = st.session_state.get('dataframe_metadata', None)

        # Generate filename suggestion
        title = metadata_base.get('title', 'experiment')
        suggested_name = title.replace(' ', '_')[:50]

        filename = st.text_input(
            "Export filename",
            value=suggested_name,
            help='Enter the filename for export. Extension will be added automatically.'
        )

        if not filename.strip():
            download_disabled = True
        else:
            download_disabled = False

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
            help="Download experiment file to your computer"
        )

        st.caption("💡 Tip: Downloaded files can be re-imported later to continue editing")