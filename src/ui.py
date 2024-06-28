import json
import os
import tempfile
import tkinter as tk
# from tkinter import *
from os import path
from tkinter import filedialog
from tkinter import Label
from PIL import Image, ImageTk
from routers.openai_module import get_gpt_extract, get_category_based_gpt_extract
# from src.pdf_extraction import extract_text_from_pdf

PAGE_CATEGORY_BASED_NLP = False

class trs_ui(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TRS AI Exploration")

        # Create a "Browse File" button
        self.browse_button = tk.Button(self.root, text="Browse TRS File", command=self.browse_file)
        self.browse_button.grid(column=0,row=0, sticky="w", columnspan=2)

        # Create a label to display the selected file
        self.file_path_label = tk.Label(self.root, text="No file selected.")
        self.file_path_label.grid(column=0, row=1, sticky="w", columnspan=2)

        # Text box for showing results
        self.text_box = tk.Text(self.root, wrap="word", font=("Arial", 12))
        self.text_box.grid(column=0,row=2, sticky="w", columnspan=2)

        # Label for Drop down
        self.image_sel_dp_label = tk.Label(self.root, text="Select Image")
        self.image_sel_dp_label.grid(column=0, row=3, sticky="w", columnspan=1)

        # Drop down
        self.image_options = ["page_1_image_1.jpg",
                              "page_2_image_1.jpg",
                              "page_3_image_1.jpg",
                              "page_3_image_2.jpg",
                              "page_4_image_1.jpg",
                              "page_5_image_1.jpg",
                              "page_5_image_2.jpg",
                              "page_5_image_3.jpg",
                              "page_6_image_1.jpg",
                              "page_6_image_2.jpg",
                              "page_6_image_3.jpg",
                              "page_7_image_1.jpg",
                              "page_7_image_2.jpg",
                              "page_7_image_3.jpg",
                              "page_8_image_1.jpg",
                              "page_9_image_1.jpg",
                              "page_10_image_1.jpg",
                              "page_11_image_1.jpg"]
        self.current_image_name = tk.StringVar(self.root)
        self.current_image_name.set(self.image_options[0])

        self.image_sel_dp = tk.OptionMenu(self.root, self.current_image_name, *self.image_options,
                                          command=self.option_changed)
        self.image_sel_dp.grid(column=1, row=3, sticky="w", columnspan=1)

        #self.image_sel_dp = tk.Button(self.root, text="Update", command=self.chage_image)
        #self.image_sel_dp.grid(column=2, row=3, sticky="w", columnspan=1)

        # Drop down for showing OCR images
        # Create a label to hold the image
        # Load the image using Pillow
        temp_directory = os.getcwd()
        image_path = path.join(temp_directory, "Images", "Picture1.png")
        print(f"image_path === {image_path}")
        image = Image.open(image_path)
        image = image.resize((500, 500))
        # Convert the image to a Tkinter-compatible image
        tk_image = ImageTk.PhotoImage(image)

        self.image_label = Label(self.root, image=tk_image)
        self.image_label.image = tk_image
        self.image_label.grid(column=0, row=4, sticky="w", columnspan=2)

        # Define tags for color coding
        self.text_box.tag_config('brace', foreground='purple')
        self.text_box.tag_config('bracket', foreground='purple')
        self.text_box.tag_config('key', foreground='blue')
        self.text_box.tag_config('string', foreground='green')
        self.text_box.tag_config('number', foreground='orange')
        self.text_box.tag_config('boolean', foreground='red')
        self.text_box.tag_config('null', foreground='gray')
        self.text_box.tag_config('comma', foreground='black')

        # Dict to store image name against the OCR obj
        self.image_vs_ocr_obj_dict = {}

    def option_changed(self, event):
        selected_option = self.current_image_name.get()
        print(f"Selected option: {selected_option}")
        # Add your callback logic here
        self.chage_image(selected_option)

    # def update_options(self, new_options):
    #     self.image_sel_dp.children["menu"].delete(0, "end")
    #     self.image_options = []
    #     for option in new_options:
    #         image_option(option, self.image_options)
    #         print(f"Adding option {option}")
    #         self.image_sel_dp.children["menu"].add_command(label=option, command=self.option_changed(None))#command=lambda opt=option: self.current_image_name.set(opt))
    #     #self.current_image_name.set(self.image_options[0])

    def chage_image(self, option):
        ocr_obj = self.image_vs_ocr_obj_dict[option]
        image_path = ocr_obj.get_image_with_ocr_boxes()
        image = Image.open(image_path)
        image = image.resize((1000, 1000))
        # Convert the image to a Tkinter-compatible image
        tk_image = ImageTk.PhotoImage(image)
        #self.image_label = Label(self.root, image=tk_image)
        self.image_label.image = tk_image
        print(f"New image to set is {option} {image_path}")

    def browse_file(self):
        # Empty result box
        self.text_box.delete('1.0', tk.END)  # Clear existing text

        filename = filedialog.askopenfilename()
        if filename:
            self.file_path_label.config(text="Selected file: " + filename)
        else:
            self.file_path_label.config(text="No file selected.")

        # Treat the pdf
        # data = extract_text_from_pdf(filename)
        if PAGE_CATEGORY_BASED_NLP:
            data = get_category_based_gpt_extract(filename)
        else:
            data, image_ocr_objects = get_gpt_extract(filename)
            #arr = []
            for each_ocr_obj in image_ocr_objects:
                name = each_ocr_obj.get_image_name()
                #arr.append(name)
                self.image_vs_ocr_obj_dict[name] = each_ocr_obj

            # Update the dropdown
            #self.update_options(arr)


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

