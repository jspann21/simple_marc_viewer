# MARC Record Viewer

MARC Record Viewer is a desktop application built with PyQt5 for viewing MARC (Machine-Readable Cataloging) records. It supports drag-and-drop functionality for various MARC file formats, including `.mrc`, `.marc`, `.001`, `.dat`, and `.txt`.

## Features

- **Drag and Drop:** Easily load MARC files by dragging and dropping them into the application window.
- **Supported Formats:** Supports MARC binary, MARCXML, MARC-in-JSON, and MARC Mnemonic formats.
- **User-Friendly Interface:** A simple and clean interface to view and parse MARC records.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/jspann21/simple_marc_viewer.git
    cd simple_marc_viewer
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python marcview.py
    ```

## Usage

1. Start the application by running the `marcview.py` script.
2. Drag and drop a MARC file into the application window.
3. The content of the MARC file will be displayed in a human-readable format.

## Requirements

- Python 3.6+
- PyQt5
- pymarc

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
