import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
import win32clipboard


def list_directories(base_path, show_files=False, level=0, output_lines=None):
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
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_lines = list_directories(folder_selected, show_files_var.get())
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)

        for line, tag in output_lines:
            text_area.insert(tk.END, line + "\n", tag)

        text_area.config(state=tk.DISABLED)


def copy_to_clipboard():
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

app.mainloop()
