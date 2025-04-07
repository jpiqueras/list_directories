"""
This script provides a graphical user interface (GUI) application for listing directories and optionally files
within a selected folder. The application allows users to browse for a folder, view its contents in a text area,
and copy the formatted output to the clipboard in Rich Text Format (RTF).
Modules:
    - os: For interacting with the file system.
    - tkinter: For creating the GUI.
    - win32clipboard: For interacting with the Windows clipboard.
Functions:
    - list_directories(base_path, show_files=False, level=0, output_lines=None):
    - browse_folder():
        Opens a folder selection dialog and displays the directory listing in the text area.
    - copy_to_clipboard():
        Converts the text area content to RTF format and copies it to the clipboard.
    - set_clipboard_rtf(rtf_text):
        Sets the clipboard content to the provided RTF text.
GUI Components:
    - Checkbutton: Allows users to toggle the inclusion of files in the directory listing.
    - Button: Provides options to select a folder and copy the output to the clipboard.
    - ScrolledText: Displays the directory listing with formatting for folders and files.
Usage:
    Run the script to launch the GUI application. Use the "Select Folder" button to choose a directory,
    and view its contents in the text area. Optionally, check the "Include files" checkbox to include files
    in the listing. Use the "Copy to Clipboard" button to copy the formatted output to the clipboard.
"""

import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import win32clipboard


def list_directories(base_path, show_files=False, level=0, output_lines=None):
    """
    Recursively lists directories and optionally files in a given base path.
    Args:
        base_path (str): The root directory path to start listing from.
        show_files (bool, optional): If True, includes files in the output. Defaults to False.
        level (int, optional): The current depth level of recursion, used for indentation. Defaults to 0.
        output_lines (list, optional): A list to store the output lines. If None, a new list is created. Defaults to None.
    Returns:
        list: A list of tuples where each tuple contains:
              - A string representing the directory or file name with indentation.
              - A string indicating the type ("folder" or "file").
    """
    if output_lines is None:
        output_lines = []

    for entry in sorted(
        os.scandir(base_path), key=lambda e: (not e.is_dir(), e.name.lower())
    ):
        indent = "\t" * level  # Use tab characters for indentation
        if entry.is_dir():
            output_lines.append((f"{indent}{entry.name}/", "folder"))
            list_directories(entry.path, show_files, level + 1, output_lines)
        elif show_files:
            output_lines.append((f"{indent}{entry.name}", "file"))

    return output_lines


def browse_folder():
    """
    Opens a folder selection dialog for the user to choose a directory. If a folder is selected,
    it lists the directories and optionally files within the selected folder. The output is
    displayed in a text area widget with appropriate tags for formatting.
    The function performs the following steps:
    1. Opens a folder selection dialog using `filedialog.askdirectory()`.
    2. If a folder is selected:
        - Calls `list_directories()` to retrieve the directory and file listing.
        - Clears the text area widget and inserts the output lines with tags.
        - Disables the text area to make it read-only.
    Dependencies:
        - `filedialog.askdirectory()`: For folder selection.
        - `list_directories(folder, show_files)`: A function to list directories and files.
        - `text_area`: A Tkinter text widget for displaying the output.
        - `show_files_var.get()`: A variable indicating whether to include files in the listing.
    Note:
        Ensure that `list_directories()` and `text_area` are properly defined and initialized
        before calling this function.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_lines = list_directories(folder_selected, show_files_var.get())
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)

        for line, tag in output_lines:
            text_area.insert(tk.END, line + "\n", tag)

        text_area.config(state=tk.DISABLED)


def copy_to_clipboard():
    """
    Generates RTF (Rich Text Format) content from the text in a text area widget and copies it to the clipboard.
    The function processes each line of text from the text area, applying specific formatting:
    - Lines ending with a "/" are styled in bold and black color.
    - Other lines are styled in blue color.
    Tabs in the text are replaced with four spaces for consistent formatting.
    The resulting RTF content is then set to the clipboard using the `set_clipboard_rtf` function.
    Note:
        This function assumes the existence of a `text_area` widget and a `set_clipboard_rtf` function.
    """
    text_lines = text_area.get("1.0", tk.END).splitlines()
    rtf_text = "{\\rtf1\\ansi\n"
    rtf_text = "{\\rtf1\\ansi\n{\\colortbl;\\red0\\green0\\blue255;\\red0\\green0\\blue0;}\n"  # blue (cf0) and black (cf1)

    for line in text_lines:
        if line.strip().endswith("/"):
            rtf_text += "\\b\\cf1 " + line.replace("\t", "    ") + "\\b0\\par\n"
        else:
            rtf_text += "\\cf0 " + line.replace("\t", "    ") + "\\par\n"

    rtf_text += "}"
    set_clipboard_rtf(rtf_text)


def set_clipboard_rtf(rtf_text):
    """
    Sets the clipboard content to the provided RTF (Rich Text Format) text.

    This function encodes the given RTF text using the ISO-8859-1 encoding
    and places it into the system clipboard as "Rich Text Format" data.

    Args:
        rtf_text (str): The RTF text to be set in the clipboard.

    Raises:
        pywintypes.error: If there is an issue interacting with the Windows clipboard.
    """
    rtf_data = rtf_text.encode(
        "ISO-8859-1", errors="replace"
    )  # Ensure the text is encoded in UTF-8
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(
        win32clipboard.RegisterClipboardFormat("Rich Text Format"), rtf_data
    )
    win32clipboard.CloseClipboard()


app = tk.Tk()
app.title("Directory Lister")
app.geometry("600x400")
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

frame = tk.Frame(app)
frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

show_files_var = tk.BooleanVar()
chk = tk.Checkbutton(frame, text="Include files", variable=show_files_var)
chk.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame, text="Select Folder", command=browse_folder)
btn_browse.pack(side=tk.LEFT, padx=5)

text_area = scrolledtext.ScrolledText(
    app, width=70, height=20, font=("Courier", 10), wrap="none"
)
text_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
text_area.tag_configure("folder", foreground="blue", font=("Courier", 10, "bold"))
text_area.tag_configure("file", foreground="black")
text_area.config(state=tk.DISABLED)

btn_copy = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)
btn_copy.grid(row=2, column=0, pady=5)

if __name__ == "__main__":
    # Start the Tkinter main loop
    app.mainloop()
