
import zipfile


class DataCiteToOpenDataSwissConverter:
    def __init__(self, input_zip, output_zip="opendataswiss.zip"):
        self.input_zip = input_zip
        self.output_zip = output_zip

    def validate_input_zip(self):
        """Validate input zip file. Raise exception if input zip file is invalid."""
        if not zipfile.is_zipfile(self.input_zip):
            raise ValueError("Input zip file not valid.")


# TODO remove
# Tests
converter = DataCiteToOpenDataSwissConverter("doi_wsl.zip")
converter.validate_input_zip()

