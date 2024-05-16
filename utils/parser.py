import json
import csv
import os
import streamlit as st
from zipfile import ZipFile, ZIP_DEFLATED
from zipfile import Path as ZPath

class TemplatesReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = self.read()

    def read(self):
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

    def read_metadata(self):
        return self.file.read_metadata()

    def detect_format(self):
        if self.file_path.endswith('.json'):
            return 'json'
        elif self.file_path.endswith('.csv'):
            return 'csv'
        elif self.file_path.endswith('.eln'):
            return 'eln'
        else:
            raise ValueError("Unknown file format")

class JSONTemplatesReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.template = self.parse()

    def parse(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def read_metadata(self) -> dict:
        return json.loads(self.template['metadata'])

class CSVTemplatesReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        templates = []
        with open(self.file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                templates.append(row)
        return templates

    def read_metadata(self):
        # CSV does not support metadata, returning an empty dictionary
        return {}

class ELNTemplatesReader:
    METADATA_FILE = 'ro-crate-metadata.json'

    def __init__(self, file_path):
        self.file_path = file_path
        self.template = self.parse()

    def parse(self):
        try:
            with ZipFile(self.file_path, "r", compression=ZIP_DEFLATED) as elnFile:
                p = ZPath(elnFile)
                dirName = sorted(p.iterdir())[0]
                metadataJsonFile = dirName.joinpath(self.METADATA_FILE)
                metadataContent = json.loads(metadataJsonFile.read_bytes())
                st.info(metadataContent)
        except Exception as e:
            st.error(f"An error occurred: {e}")


    def read_metadata(self):
        # ELN does not support metadata, returning an empty dictionary
        return {}
