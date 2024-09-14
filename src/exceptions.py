class InvalidFilenameError(Exception):
    def __init__(self, filename):
        self.filename = filename
        self.message = f"Invalid filename: {filename}"
        super().__init__(self.message)

class InvalidLogFormatError(Exception):
    def __init__(self, log_format):
        self.log_format = log_format
        self.message = f"Invalid log format: {log_format}"
        super().__init__(self.message)

class LookupTableError(Exception):
    def __init__(self):
        self.message = "Not a valid Lookup Table."
        super().__init__(self.message)

class EmptyFileError(Exception):
    def __init__(self, filename):
        super().__init__(f"The file '{filename}' is empty.")
        self.filename = filename