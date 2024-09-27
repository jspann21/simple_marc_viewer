"""
This module defines a GUI application for viewing MARC records.
It supports drag-and-drop functionality for various MARC formats.
"""

import sys
import traceback
from io import StringIO
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from pymarc import MARCReader, parse_xml_to_array, parse_json_to_array

# Attempt to import TextReader, use a fallback if not available
try:
    from pymarc import TextReader
except ImportError:
    TextReader = None


class MarcViewer(QMainWindow):
    """A main window class for the MARC Record Viewer application."""

    def __init__(self):
        """Initialize the main window and set up the UI components."""
        super().__init__()

        self.setWindowTitle("MARC Record Viewer")
        self.setGeometry(300, 300, 800, 600)

        # Create a central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create the text edit widget for displaying MARC records
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # Create a placeholder label for instructions
        self.placeholder_label = QLabel(
            "Drop a MARC record file here to view.\n\n"
            "Supported formats: .mrc, .marc, .001, .dat, .txt",
            self
        )
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("font-size: 16px; color: grey;")

        # Add both widgets to the layout
        self.layout.addWidget(self.placeholder_label)
        self.layout.addWidget(self.text_edit)

        # Initially show only the placeholder
        self.text_edit.hide()

        # Enable drag and drop
        self.setAcceptDrops(True)

    @staticmethod
    def dragEnterEvent(event):
        """Handle the dragEnter event to accept file drops."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle the dropEvent to load the dropped MARC file."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # Accept multiple extensions including .001
            if file_path.endswith(('.mrc', '.marc', '.001', '.dat', '.txt')):
                self.load_marc_file(file_path)

    def load_marc_file(self, file_path):
        """Load and display the content of a MARC file."""
        try:
            with open(file_path, 'rb') as marc_file:
                content = marc_file.read()

                # Hide placeholder label when a file is loaded
                self.placeholder_label.hide()
                self.text_edit.show()

                # Determine the format of the MARC file
                if self.is_marcxml(content):
                    records = parse_xml_to_array(content)
                elif self.is_json(content):
                    records = parse_json_to_array(content)
                elif self.is_mnemonic(content):
                    records = self.parse_mnemonic_records(content)
                else:
                    marc_file.seek(0)  # Reset file pointer
                    reader = MARCReader(marc_file, to_unicode=True, force_utf8=True)
                    records = list(reader)

                record_output = ""
                for record in records:
                    record_output += self.parse_record(record)
                    record_output += "\n" + "=" * 40 + "\n"
                self.text_edit.setText(record_output)
        except (UnicodeDecodeError, IOError) as e:
            error_message = (
                f"Error reading MARC file: {str(e)}\nDetails:\n{traceback.format_exc()}"
            )
            self.text_edit.setText(error_message)

    @staticmethod
    def is_marcxml(content):
        """Check if the content is in MARCXML format."""
        return content.strip().startswith(b'<?xml')

    @staticmethod
    def is_json(content):
        """Check if the content is in JSON format."""
        return content.strip().startswith(b'[') or content.strip().startswith(b'{')

    @staticmethod
    def is_mnemonic(content):
        """Check if the content is in mnemonic format."""
        return b'\n' in content and b'=' in content[:100]

    def parse_mnemonic_records(self, content):
        """Parse records in mnemonic format."""
        if not TextReader:
            return self.parse_mnemonic_records_fallback(content)

        try:
            content_str = content.decode('utf-8', errors='replace')
        except UnicodeDecodeError:
            content_str = content.decode('latin-1', errors='replace')

        # Split records by double newlines
        records_data = content_str.strip().split('\n\n')
        records = []
        for record_data in records_data:
            try:
                record = self.parse_mnemonic_record(record_data)
                records.append(record)
            except (StopIteration, TypeError):
                # Handle specific exceptions during record parsing
                pass
        return records

    @staticmethod
    def parse_mnemonic_records_fallback(content):
        """Fallback method for parsing mnemonic records without TextReader."""
        content_str = content.decode('utf-8', errors='replace')
        records_data = content_str.strip().split('\n\n')
        records = []
        for _ in records_data:
            # Implement custom parsing logic here as fallback
            record = None  # Placeholder for custom parsing
            records.append(record)
        return records

    @staticmethod
    def parse_mnemonic_record(record_data):
        """Parse a single mnemonic record."""
        if TextReader:
            reader = TextReader(StringIO(record_data))
            record = next(reader)
            return record
        return None  # If TextReader is not available, return None

    @staticmethod
    def parse_record(record):
        """Parse a single MARC record into a readable format."""
        try:
            output = f"Record ID: {record['001'].value() if '001' in record else 'No ID'}\n"
            for field in record.get_fields():
                if field.is_control_field():
                    output += f"{field.tag}: {field.data}\n"
                else:
                    subfields = ' '.join(
                        f"{subfield.code} {subfield.value}" for subfield in field.subfields
                    )
                    output += (
                        f"{field.tag:<4} {field.indicators[0]}{field.indicators[1]} "
                        f"{subfields}\n"
                    )
            return output
        except (KeyError, AttributeError) as e:
            error_message = (
                f"Error parsing record: {str(e)}\nDetails:\n{traceback.format_exc()}"
            )
            return error_message


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MarcViewer()
    viewer.show()
    sys.exit(app.exec_())
