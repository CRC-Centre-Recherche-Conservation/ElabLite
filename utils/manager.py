import csv
import dill as pickle
import os
import pandas as pd
import streamlit as st
import zipfile
from io import BytesIO
from pandas import DataFrame
from tempfile import NamedTemporaryFile, gettempdir
from typing import Dict


def manage_temp_dir(child: str = None) -> str:
    """
    Function to manage tmp dir templates/ and get the 10 files most recent and remove the rest
    :param child: str, optional child directory in tmp dir
    :return: str, path tmp/templates/
    """
    temp_dir = gettempdir()
    if child is None:
        templates_dir = os.path.join(temp_dir, "templates")
    else:
        templates_dir = os.path.join(temp_dir, "templates", child)
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    # keep only the first 10 templates recent
    templates = sorted(os.listdir(templates_dir), key=lambda x: os.path.getmtime(os.path.join(templates_dir, x)))
    while len(templates) > 10:
        os.remove(os.path.join(templates_dir, templates[0]))
        templates.pop(0)
    return templates_dir


@st.cache_data
def convert_df(df):
    """cache dataframe"""
    return df.to_csv().encode("utf-8")

@st.cache_data
def create_elablite(metadata_base: Dict, form_data: Dict, template_metadata: Dict, dataframe_metadata: pd.DataFrame) -> bytes:
    """
    Create a serialized binary representation of metadata dictionary. Content .elablite

    Args:
            metadata_base (Dict): A dictionary containing base metadata with keys 'date', 'title', 'commentary', 'rating',
                            and 'tags'. Related to Page 2 - Step 1 base metadata.
            form_data (Dict): A dictionary containing form of metadata experience.
                                Related to Page 2 - Step 2 form metadata.
            template_metadata (Dict): Dict of metadata template
            dataframe_metadata (DataFrame): DataFrame of metadata edited by analysis

    Returns:
        bytes: Serialized binary data representing the metadata dictionary.
    """
    metadata_dict = {
        '@context': 'http://example.org/elablite/v1.0/',
        'metadata_base': metadata_base,
        'form_data': form_data,
        'template_metadata': template_metadata,
        'dataframe_metadata': dataframe_metadata
    }

    return pickle.dumps(metadata_dict)


def generate_csv(base_mtda: Dict, df_mtda: DataFrame, grouped: bool) -> str:
    """
        Generates a CSV file from base metadata and a DataFrame of additional metadata.

        Args:
            base_mtda (Dict): A dictionary containing base metadata with keys 'date', 'title', 'commentary', 'rating',
                            and 'tags'. Related to Page 2 - Step 1 base metadata.
            df_mtda (pd.DataFrame): A DataFrame containing experience metadata. Related to Page 2 - Step 2 and 3 forms
                                    metadata and dataframe editor.
            grouped (bool): A boolean indicating whether the experiences and files should be bundled. Related to
                            Page 4 - button grouped.

        Returns:
            str: The file path to the generated CSV file.

        Example:
            base_mtda = {
                'date': '2024-06-06',
                'title': 'Sample Title',
                'commentary': 'Sample commentary',
                'rating': 5,
                'tags': 'sample,example'
            }
            df_mtda = pd.DataFrame({
                'extra_field1': ['value1', 'value2'],
                'extra_field2': ['value3', 'value4']
            })
            csv_filename = generate_csv(base_mtda, df_mtda, grouped=False)
        """
    headers = ['date', 'title', 'body', 'rating', 'metadata', 'tags']
    with NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv', encoding='utf-8') as csv_file:
        metadata = st.session_state['template_metadata']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        if grouped:
            for col in df_mtda.columns:
                if col in metadata['extra_fields']:
                    if metadata['extra_fields'][col]['type'] == 'number':
                        try:
                            value, unit = df_mtda[col].iloc[0].split(' ')
                        except ValueError:
                            st.warning(f"Impossible to parse the value and its unit in the column '{col}'. \
                            Please check your column content and don't use ' ' in the unit appellation.")
                        metadata['extra_fields'][col]['value'] = value
                        metadata['extra_fields'][col]['unit'] = unit
                    else:
                        metadata['extra_fields'][col]['value'] = df_mtda[col].iloc[0]
            data = {'date': base_mtda['date'], 'title': base_mtda['title'], 'body': base_mtda['commentary'],
                    'rating': base_mtda['rating'], 'metadata': metadata, 'tags': base_mtda['tags']}
            writer.writerow(data)
        else:
            for idx, row in df_mtda.iterrows():
                for col in df_mtda.columns:
                    if col in metadata['extra_fields']:
                        if metadata['extra_fields'][col]['type'] == 'number':
                            try:
                                value, unit = row[col].split(' ')
                            except ValueError:
                                st.warning(f"Impossible to parse the value and its unit in the column '{col}'. \
                                Please check your column content and don't use ' ' in the unit appellation.")
                            metadata['extra_fields'][col]['value'] = value
                            metadata['extra_fields'][col]['unit'] = unit
                        else:
                            metadata['extra_fields'][col]['value'] = row[col]
                data = {'date': base_mtda['date'], 'title': base_mtda['title'], 'body': base_mtda['commentary'],
                        'rating': base_mtda['rating'], 'metadata': metadata, 'tags': base_mtda['tags']}
                writer.writerow(data)
        csv_filename = csv_file.name
    return csv_filename


def files_management(uploaded_files: Dict[str, bytes], df_mtda: DataFrame, grouped: bool) -> Dict[
    str, Dict[str, bytes]]:
    """
    Manages the renaming and grouping of uploaded files based on metadata provided in a DataFrame.

    Args:
        uploaded_files (Dict[str, bytes]): A dictionary containing the uploaded files.
            The keys are the original filenames, and the values are the file data.
        df_mtda (pd.DataFrame): A DataFrame containing metadata for the files.
            The DataFrame must have the columns 'Filename', 'new_Filename', and 'new_title'.
        grouped (bool): A boolean indicating whether the files should be grouped together in a single dictionary.

    Returns:
        Dict[str, Dict[str, bytes]]: A dictionary with the new filenames and titles,
        containing the uploaded files data as specified by the metadata. The structure of the returned
        dictionary depends on the `grouped` parameter:
            - If `grouped` is True, returns a dictionary with a single key 'data' containing all files.
            - If `grouped` is False, returns a dictionary where each key is a 'new_title' and each value
              is another dictionary containing the files associated with that title.

    Example:
        uploaded_files = {
            'file1.txt': b'filedata1',
            'file2.txt': b'filedata2'
        }
        df_mtda = pd.DataFrame({
            'Filename': ['file1.txt', 'file2.txt'],
            'new_Filename': ['new_file1.txt', 'new_file2.txt'],
            'new_title': ['title1', 'title2']
        })
        new_dict = files_management(uploaded_files, df_mtda, grouped=False)
        # Example output:
        # {
        #     'title1': {'new_file1.txt': b'filedata1'},
        #     'title2': {'new_file2.txt': b'filedata2'}
        # }
    """
    new_dict = {}
    # Keep Filename
    if 'new_Filename' not in df_mtda.columns.tolist():
        if grouped:
            new_dict['data'] = uploaded_files
        else:
            for idx, row in df_mtda.iterrows():
                if row['new_title'] not in new_dict:
                    new_dict[row['new_title']] = {}
                new_dict[row['new_title']][row['Filename']] = uploaded_files[row['Filename']]
        return new_dict
    # New Filename
    else:
        if grouped:
            new_dict['data'] = {}
            for key, new_filename in zip(df_mtda['Filename'], df_mtda['new_Filename']):
                if key in uploaded_files:
                    new_dict['data'][new_filename] = uploaded_files[key]
        else:
            for idx, row in df_mtda.iterrows():
                if row['new_title'] not in new_dict:
                    new_dict[row['new_title']] = {}
                new_dict[row['new_title']][row['new_Filename']] = uploaded_files[row['Filename']]
        return new_dict


def zip_experience(csv_filename: str, uploaded_files: Dict[str, Dict[str, bytes]], logs_process: bytes) -> BytesIO:
    """
    Creates a zip archive containing a CSV file and additional uploaded files.

    Args:
        csv_filename (str): The path to the CSV file to be included in the zip archive.
        uploaded_files (Dict): A dictionary containing the files to be added to the zip archive.
            The dictionary should be in the format {folder_name: {file_name: file_data}}.
        logs_process (bytes): Edited dataframe cached to retain all modified information before transformation
            and zipping.

    Returns:
        BytesIO: A BytesIO object containing the zip archive.

    Example:
        uploaded_files = {
            'images': {
                'image1.png': b'filedata1',
                'image2.png': b'filedata2'
            },
            'documents': {
                'doc1.txt': b'filedata3',
                'doc2.txt': b'filedata4'
            }
        }
        zip_buffer = zip_experience('experiences.csv', uploaded_files, logs_process)
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(csv_filename, arcname='experiences.csv')
        zip_file.writestr('logs_process.csv', logs_process)
        for folder_name, files in uploaded_files.items():
            file_names = []
            for file_name, file_data in files.items():
                file_path = os.path.join(folder_name, file_name)
                zip_file.writestr(file_path, file_data)
                file_names.append(file_path)
            zip_file.writestr(os.path.join(folder_name, 'DATAFILE.txt'), "\n".join(file_names))
    zip_buffer.seek(0)
    os.unlink(csv_filename)
    return zip_buffer
