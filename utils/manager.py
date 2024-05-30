import csv
import datetime
import os
import zipfile
from io import BytesIO
from tempfile import NamedTemporaryFile, gettempdir

def manage_temp_dir() -> str:
    """
    Function to manage tmp dir templates/ and get the 10 files most recent and remove the rest
    :return: str, path tmp/templates/
    """
    temp_dir = gettempdir()
    templates_dir = os.path.join(temp_dir, "templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    # keep only the first 10 templates recent
    templates = sorted(os.listdir(templates_dir), key=lambda x: os.path.getmtime(os.path.join(templates_dir, x)))
    while len(templates) > 10:
        os.remove(os.path.join(templates_dir, templates[0]))
        templates.pop(0)
    return templates_dir


def generate_experience(filename: str, experiences: list):
    headers = [
        'date', 'title', 'body', 'category', 'category_title', 'category_color',
        'status', 'status_title', 'status_color', 'custom_id', 'rating',
        'metadata', 'tags'
    ]

    with NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        # looping writerow on experiences list ...

        csv_filename = csv_file.name

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(csv_filename, arcname='experiences.csv')
    zip_buffer.seek(0)

    os.unlink(csv_file.name)

    return zip_buffer

