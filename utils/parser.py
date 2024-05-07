import json
import csv

class TemplatesReader:
    def __init__(self, file_path):
        self.file_path = file_path

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
        return reader.parse()

    def read_metadata(self):
        file_format = self.detect_format()
        if file_format == 'json':
            reader = JSONTemplatesReader(self.file_path)
        elif file_format == 'csv':
            reader = CSVTemplatesReader(self.file_path)
        elif file_format == 'eln':
            reader = ELNTemplatesReader(self.file_path)
        else:
            raise ValueError("Unsupported file format")
        return reader.read_metadata()

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

    def parse(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def read_metadata(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            return data.get('metadata', {})

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

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        # Placeholder for ELN parsing logic
        return "ELN parsing not implemented yet"

    def read_metadata(self):
        # ELN does not support metadata, returning an empty dictionary
        return {}
