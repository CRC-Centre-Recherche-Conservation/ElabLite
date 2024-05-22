import os
import tempfile


def manage_temp_dir() -> str:
    """
    Function to manage tmp dir templates/ and get the 10 files most recent and remove the rest
    :return: str, path tmp/templates/
    """
    temp_dir = tempfile.gettempdir()
    templates_dir = os.path.join(temp_dir, "templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    # keep only the first 10 templates recent
    templates = sorted(os.listdir(templates_dir), key=lambda x: os.path.getmtime(os.path.join(templates_dir, x)))
    while len(templates) > 10:
        os.remove(os.path.join(templates_dir, templates[0]))
        templates.pop(0)
    return templates_dir

