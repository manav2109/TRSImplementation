import json
import tkinter as tk
from tkinter import filedialog

from routers.openai_module import get_gpt_extract, get_category_based_gpt_extract
# from src.pdf_extraction import extract_text_from_pdf

PAGE_CATEGORY_BASED_NLP = False


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

        # Define tags for color coding
        self.text_box.tag_config('brace', foreground='purple')
        self.text_box.tag_config('bracket', foreground='purple')
        self.text_box.tag_config('key', foreground='blue')
        self.text_box.tag_config('string', foreground='green')
        self.text_box.tag_config('number', foreground='orange')
        self.text_box.tag_config('boolean', foreground='red')
        self.text_box.tag_config('null', foreground='gray')
        self.text_box.tag_config('comma', foreground='black')

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
        if PAGE_CATEGORY_BASED_NLP:
            data = get_category_based_gpt_extract(filename)
        else:
            data = get_gpt_extract(filename)

        self.set_text_data(data)
        return filename

    def set_text_data(self, data):
        beautified_json = json.dumps(data, indent=4)
        # # Display the beautified JSON in the Text widget
        # self.text_box.delete("1.0", tk.END)  # Clear existing text
        # self.text_box.insert(tk.END, beautified_json)
        self.pretty_print_json(beautified_json)

    def start_ui(self):
        # Run the main event loop
        self.root.mainloop()

    def pretty_print_json(self, data):
        self.text_box.delete(1.0, tk.END)  # Clear existing content

        def insert_with_tag(content, tag):
            self.text_box.insert(tk.END, content, tag)

        def recursive_insert(json_obj, indent=0):
            indent_str = ' ' * indent
            if isinstance(json_obj, dict):
                insert_with_tag('{\n', 'brace')
                for i, (key, value) in enumerate(json_obj.items()):
                    insert_with_tag(f'{indent_str}  "{key}": ', 'key')
                    recursive_insert(value, indent + 2)
                    if i < len(json_obj) - 1:
                        insert_with_tag(',\n', 'comma')
                    else:
                        insert_with_tag('\n', 'brace')
                insert_with_tag(f'{indent_str}}}', 'brace')
            elif isinstance(json_obj, list):
                insert_with_tag('[\n', 'bracket')
                for i, item in enumerate(json_obj):
                    insert_with_tag(indent_str + '  ', None)
                    recursive_insert(item, indent + 2)
                    if i < len(json_obj) - 1:
                        insert_with_tag(',\n', 'comma')
                    else:
                        insert_with_tag('\n', 'bracket')
                insert_with_tag(f'{indent_str}]', 'bracket')
            elif isinstance(json_obj, str):
                insert_with_tag(f'"{json_obj}"', 'string')
            elif isinstance(json_obj, (int, float)):
                insert_with_tag(str(json_obj), 'number')
            elif isinstance(json_obj, bool):
                insert_with_tag(str(json_obj).lower(), 'boolean')
            elif json_obj is None:
                insert_with_tag('null', 'null')

        json_obj = json.loads(data)
        recursive_insert(json_obj)

