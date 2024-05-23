import json
import tkinter as tk
from tkinter import filedialog

from routers.openai_module import get_gpt_extract
from src.pdf_extraction import extract_text_from_pdf


class trs_ui(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRS AI Exploration")

        # Create a label to display the selected file
        self.label = tk.Label(self.root, text="No file selected.")
        self.label.pack(pady=10)

        # Create a "Browse File" button
        self.browse_button = tk.Button(self.root, text="Browse File", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Text box for showing results
        self.text_box = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.text_box.pack(expand=True, fill="both")

    def browse_file(self):
        # Empty result box
        self.text_box.delete('1.0', tk.END)  # Clear existing text

        filename = filedialog.askopenfilename()
        if filename:
            self.label.config(text="Selected file: " + filename)
        else:
            self.label.config(text="No file selected.")

        # Treat the pdf
        # data = extract_text_from_pdf(filename)
        data = get_gpt_extract(filename)

        self.set_text_data(data)
        return filename

    def set_text_data(self, data):
        beautified_json = json.dumps(data, indent=4)
        # Display the beautified JSON in the Text widget
        self.text_box.delete("1.0", tk.END)  # Clear existing text
        self.text_box.insert(tk.END, beautified_json)

    def start_ui(self):
        # Run the main event loop
        self.root.mainloop()
