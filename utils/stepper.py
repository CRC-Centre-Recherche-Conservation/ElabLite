import streamlit as st


class WorkflowStepper:
    """
    Component to display workflow progress with a stepper bar
    """

    STEPS = [
        {"key": "step_metadata_base", "label": "Base", "icon": "📝"},
        {"key": "step_metadata_forms", "label": "Metadata", "icon": "📋"},
        {"key": "step_metadata_files", "label": "Files", "icon": "📁"},
        {"key": "step_metadata_download", "label": "Export", "icon": "💾"}
    ]

    PRESET_STEPS = [
        {"key": "preset_metadata_base", "label": "Base", "icon": "📝"},
        {"key": "preset_metadata_forms", "label": "Metadata", "icon": "📋"},
        {"key": "preset_metadata_files", "label": "Files", "icon": "📂"},
        {"key": "preset_metadata_download", "label": "Export", "icon": "💾"}
    ]

    @staticmethod
    def render(current_step: str, step_type: str = "step"):
        """
        Render the stepper bar

        Args:
            current_step: Current step key (e.g., 'step_metadata_base')
            step_type: Type of steps ('step' or 'preset')
        """
        steps = WorkflowStepper.STEPS if step_type == "step" else WorkflowStepper.PRESET_STEPS

        # Get current step index
        current_index = next((i for i, s in enumerate(steps) if s["key"] == current_step), 0)

        # Custom CSS for stepper
        st.markdown("""
        <style>
        .stepper-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
            padding: 15px;
            background: linear-gradient(to right, #f0f2f6 0%, #ffffff 100%);
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
        }

        .step-circle {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            z-index: 2;
            transition: all 0.3s ease;
        }

        .step-circle.completed {
            background: linear-gradient(135deg, #096a2e 0%, #0a8f3d 100%);
            color: white;
            box-shadow: 0 4px 8px rgba(9, 106, 46, 0.3);
        }

        .step-circle.active {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: 3px solid #096a2e;
            box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
            transform: scale(1.1);
        }

        .step-circle.pending {
            background: #e0e0e0;
            color: #9e9e9e;
            border: 2px solid #bdbdbd;
        }

        .step-label {
            margin-top: 8px;
            font-size: 13px;
            font-weight: 600;
            text-align: center;
        }

        .step-label.completed {
            color: #096a2e;
        }

        .step-label.active {
            color: #4CAF50;
            font-weight: 700;
        }

        .step-label.pending {
            color: #9e9e9e;
        }

        .step-connector {
            position: absolute;
            top: 22px;
            left: 50%;
            width: 100%;
            height: 3px;
            z-index: 1;
        }

        .step-connector.completed {
            background: linear-gradient(to right, #096a2e 0%, #0a8f3d 100%);
        }

        .step-connector.pending {
            background: #e0e0e0;
        }

        .step:last-child .step-connector {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

        # Build stepper HTML
        html_parts = ['<div class="stepper-container">']

        for i, step in enumerate(steps):
            # Determine step state
            if i < current_index:
                state = "completed"
                icon = "✓"
            elif i == current_index:
                state = "active"
                icon = step["icon"]
            else:
                state = "pending"
                icon = step["icon"]

            # Connector state
            connector_state = "completed" if i < current_index else "pending"

            # Build step HTML with proper escaping
            step_html = (
                f'<div class="step">'
                f'<div class="step-circle {state}">{icon}</div>'
                f'<div class="step-label {state}">{step["label"]}</div>'
                f'<div class="step-connector {connector_state}"></div>'
                f'</div>'
            )
            html_parts.append(step_html)

        html_parts.append('</div>')
        html = ''.join(html_parts)

        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def get_progress_percentage(current_step: str, step_type: str = "step") -> int:
        """
        Calculate progress percentage

        Args:
            current_step: Current step key
            step_type: Type of steps ('step' or 'preset')

        Returns:
            int: Progress percentage (0-100)
        """
        steps = WorkflowStepper.STEPS if step_type == "step" else WorkflowStepper.PRESET_STEPS
        current_index = next((i for i, s in enumerate(steps) if s["key"] == current_step), 0)
        return int(((current_index + 1) / len(steps)) * 100)
