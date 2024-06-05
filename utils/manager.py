import csv
import datetime
import os
import streamlit as st
import zipfile
from io import BytesIO
from pandas import DataFrame
from tempfile import NamedTemporaryFile, gettempdir
from typing import Dict


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


def generate_csv(base_mtda: Dict, df_mtda: DataFrame, grouped: bool) -> str:
    headers = ['date', 'title', 'body', 'rating', 'metadata', 'tags']
    with NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv', encoding='utf-8') as csv_file:
        metadata = st.session_state['template_metadata']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        if grouped:
            for col in df_mtda.columns:
                if col in metadata['extra_fields']:
                    metadata['extra_fields'][col]['value'] = df_mtda[col].iloc[0]
            data = {'date': base_mtda['date'], 'title': base_mtda['title'], 'body': base_mtda['commentary'],
                    'rating': base_mtda['rating'], 'metadata': metadata, 'tags': base_mtda['tags']}
            writer.writerow(data)
        else:
            for idx, row in df_mtda.iterrows():
                for col in df_mtda.columns:
                    if col in metadata['extra_fields']:
                        metadata['extra_fields'][col]['value'] = row[col]
                data = {'date': base_mtda['date'], 'title': base_mtda['title'], 'body': base_mtda['commentary'],
                        'rating': base_mtda['rating'], 'metadata': metadata, 'tags': base_mtda['tags']}
                writer.writerow(data)
        csv_filename = csv_file.name
    return csv_filename


def files_management(uploaded_files: Dict, df_mtda: DataFrame, grouped: bool) -> Dict:
    new_dict = {}
    if grouped:
        for key, new_filename in zip(df_mtda['Filename'], df_mtda['new_Filename']):
            if key in uploaded_files:
                new_dict['data'] = {new_filename: uploaded_files[key]}
    else:
        for idx, row in df_mtda.iterrows():
            new_dict[row['new_title']] = {row['new_Filename']: uploaded_files[row['Filename']]}
    return new_dict


def zip_experience(csv_filename: str) -> BytesIO:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(csv_filename, arcname='experiences.csv')
    zip_buffer.seek(0)
    os.unlink(csv_filename)
    return zip_buffer
