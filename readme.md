# Directory Lister

A graphical user interface (GUI) application for listing directories and optionally files within a selected folder. The application allows users to browse for a folder, view its contents in a text area, and copy the formatted output to the clipboard in Rich Text Format (RTF).

## Features

- **Directory Listing**: Recursively lists directories and optionally files in a selected folder.
- **Rich Text Format (RTF) Output**: Copies the formatted directory listing to the clipboard in RTF format.
- **Customizable Output**: Toggle the inclusion of files in the directory listing.
- **User-Friendly GUI**: Built with Tkinter for a simple and intuitive interface.

## Requirements

- Python 3.8 or higher
- Required Python modules:
  - `tkinter` (built-in with Python)
  - `pywin32` (for clipboard interaction on Windows)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/list-directories.git
   cd list-directories
   ```

2. Install dependencies:
   ```bash
   pip install pywin32
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Use the GUI to:
   - Click **Select Folder** to choose a directory.
   - Check **Include files** to include files in the listing.
   - View the directory structure in the text area.
   - Click **Copy to Clipboard** to copy the formatted output in RTF format.

## How It Works

1. **Directory Listing**: The `list_directories` function recursively scans the selected folder and generates a formatted list of directories and files.
2. **GUI Interaction**: The application uses Tkinter components like `Checkbutton`, `Button`, and `ScrolledText` for user interaction.
3. **Clipboard Integration**: The `copy_to_clipboard` function converts the directory listing to RTF format and uses `win32clipboard` to copy it to the clipboard.

## Example Output

### Text Area
```
Folder1/
    Subfolder1/
    Subfolder2/
        File1.txt
        File2.txt
```

### RTF Clipboard Output
- Folders are bold and black.
- Files are blue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- **Javier Piqueras**  
  [javier.piqueras@upm.es](mailto:javier.piqueras@upm.es)