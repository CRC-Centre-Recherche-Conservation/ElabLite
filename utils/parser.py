import json
import csv
import streamlit as st
from typing import Dict, List
from zipfile import ZipFile, ZIP_DEFLATED
from zipfile import Path as ZPath


class TemplatesReader:
    """Generic class to read templates"""

    def __init__(self, file_path: str):
        """
        :param file_path: str, path of your file
        """
        self.file_path = file_path
        self.file = self.read()

    def read(self):
        """
        Reads the file according to its format by creating an appropriate reader instance.
        :return: instance reader of specific class
        """
        file_format = self.detect_format()
        if file_format == 'json':
            reader = JSONTemplatesReader(self.file_path)
        elif file_format == 'csv':
            reader = CSVTemplatesReader(self.file_path)
        elif file_format == 'eln':
            reader = ELNTemplatesReader(self.file_path)
        else:
            raise ValueError("Unsupported file format")
        return reader

    def read_metadata(self) -> Dict:
        """
        Reads the metadata from the file using the specific reader instance.
        :return: dict: Metadata of the file.
        """
        return self.file.read_metadata()

    def detect_format(self) -> str:
        """
        Detects the format of the file based on its extension.
        :return: str, format file or raise ValueError
        """
        if self.file_path.endswith('.json'):
            return 'json'
        elif self.file_path.endswith('.csv'):
            return 'csv'
        elif self.file_path.endswith('.eln'):
            return 'eln'
        elif self.file_path.endswith('.elablite'):
            return 'elablite'
        else:
            raise ValueError("Unknown file format")


class JSONTemplatesReader:

    def __init__(self, file_path: str):
        """Initializes the JSONTemplatesReader object.
        :param file_path: str, Path to the JSON template file.
        """
        self.file_path = file_path
        self.template = self.parse()

    def parse(self) -> Dict:
        """
        Parses the JSON file and loads the content.
        :return: dict, Parsed JSON content
        """
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def read_metadata(self) -> Dict:
        """
        Reads the metadata from the JSON file.
        :return: dict, Metadata extracted from the JSON content.
        """
        return json.loads(self.template['metadata'])


class CSVTemplatesReader:

    def __init__(self, file_path: str):
        """
        Initializes the CSVTemplatesReader object.
        :param file_path: str, Path to the CSV template file.
        """
        self.file_path = file_path

    def parse(self) -> List[str]:
        """
        Parses the CSV file and loads the content as a list of dictionaries.
        :return: list[str]: List of rows.
        """
        templates = []
        with open(self.file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                templates.append(row)
        return templates

    def read_metadata(self) -> Dict:
        """
        Reads the metadata from the CSV file.
        :return:
        """
        # CSV does not support metadata, returning an empty dictionary
        return {}


class ELNTemplatesReader:
    METADATA_FILE = 'ro-crate-metadata.json'

    def __init__(self, file_path: str):
        """
        Initializes the ELNTemplatesReader object.
        :param file_path: str, Path to the ELN template file.
        """
        self.file_path = file_path
        self.template = self.parse()

    def parse(self):
        """
        Parses the ELN file, extracts, and displays metadata.
        :return:
        """
        try:
            with ZipFile(self.file_path, "r", compression=ZIP_DEFLATED) as elnFile:
                p = ZPath(elnFile)
                dirName = sorted(p.iterdir())[0]
                metadataJsonFile = dirName.joinpath(self.METADATA_FILE)
                metadataContent = json.loads(metadataJsonFile.read_bytes())
                st.info(metadataContent)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        st.warning('ELN format not yet available')

    def read_metadata(self) -> Dict:
        """
        Reads the metadata from the ELN file.
        :return:
        """
        st.warning('ELN format not yet available')

class ElabLiteTemplatesReader:

    def __init__(self, file_path: str):
        """
        Initializes the ElabLiteTemplatesReader object. MIME/TYPE : application/json
        :param file_path: str, Path to the ElabLite template file.
        """
        self.file_path = file_path
        self.template = self.parse()

    def parse(self):
        """
        Parses the ElabLite file, extracts, and displays metadata.
        :return:
        """
        st.warning('ElabLite format not yet available')

    def read_metadata(self) -> Dict:
        """
        Reads the metadata from the ElabLite file.
        :return:
        """
        st.warning('ElabLite format not yet available')