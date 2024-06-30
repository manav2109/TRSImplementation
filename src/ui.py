import json
from tkinter import filedialog, Label, Tk, Text, StringVar, OptionMenu, Button, Canvas, Scrollbar, NW
from routers.openai_module import get_gpt_extract, get_category_based_gpt_extract
from PIL import Image, ImageTk

PAGE_CATEGORY_BASED_NLP = False

class trs_ui(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("TRS AI Exploration")

        # Configure the grid layout to expand properly
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(4, weight=1)

        # Create a "Browse File" button
        self.browse_button = Button(self.root, text="Browse TRS File", command=self.browse_file)
        self.browse_button.grid(column=0, row=0, sticky="w", columnspan=2)

        # Create a label to display the selected file
        self.file_path_label = Label(self.root, text="No file selected.")
        self.file_path_label.grid(column=0, row=1, sticky="w", columnspan=2)

        # Text box for showing results
        self.text_box = Text(self.root, wrap="word", font=("Arial", 12))
        self.text_box.grid(column=0, row=2, sticky="nsew", columnspan=2)

        # Label for Drop down
        self.image_sel_dp_label = Label(self.root, text="Select Image")
        self.image_sel_dp_label.grid(column=0, row=3, sticky="w", columnspan=1)

        # Drop down
        self.current_image_name = StringVar(self.root)
        self.current_image_name.set("No images available")  # Default value
        self.image_sel_dp = OptionMenu(self.root, self.current_image_name, "No images available",
                                       command=self.option_changed)
        self.image_sel_dp.grid(column=1, row=3, sticky="w", columnspan=1)

        # Canvas for displaying image
        self.canvas = Canvas(self.root, bg='white')
        self.canvas.grid(column=0, row=4, sticky="nsew", columnspan=2)

        # Scrollbars
        self.vbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.vbar.grid(row=4, column=2, sticky="ns")
        self.hbar = Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.hbar.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # Bind mouse events for zoom and pan
        self.canvas.bind("<ButtonPress-1>", self.pan_start)
        self.canvas.bind("<B1-Motion>", self.pan_move)
        self.canvas.bind("<MouseWheel>", self.zoom)

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
        self.image_cache = {}
        self.img = None
        self.img_id = None
        self.zoom_factor = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0

    def option_changed(self, event=None):
        selected_option = self.current_image_name.get()
        self.change_image(selected_option)

    def change_image(self, option):
        ocr_obj = self.image_vs_ocr_obj_dict.get(option)
        if ocr_obj:
            image_path = ocr_obj.get_image_with_ocr_boxes()
            self.img = Image.open(image_path)
            self.update_image()

    def update_image(self):
        if self.img:
            width, height = self.img.size
            resized_image = self.img.resize((int(width * self.zoom_factor), int(height * self.zoom_factor)),
                                            Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            self.img_id = self.canvas.create_image(0, 0, anchor=NW, image=tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox(self.img_id))
            self.canvas.image = tk_image  # Keep a reference to avoid garbage collection

    def pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_factor *= 1.1
        elif event.delta < 0:
            self.zoom_factor /= 1.1
        self.update_image()

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path_label.config(text="Selected file: " + filename)
        else:
            self.file_path_label.config(text="No file selected.")

        # Treat the pdf
        if PAGE_CATEGORY_BASED_NLP:
            data = get_category_based_gpt_extract(filename)
        else:
            data, image_ocr_objects = get_gpt_extract(filename)
            image_names = []
            for each_ocr_obj in image_ocr_objects:
                if len(each_ocr_obj.ocr_text) > 1:
                    name = each_ocr_obj.get_image_name()
                    image_names.append(name)
                    self.image_vs_ocr_obj_dict[name] = each_ocr_obj

            # Update the dropdown with new image names
            self.update_options(image_names)

        self.set_text_data(data)
        return filename

    def update_options(self, new_options):
        menu = self.image_sel_dp["menu"]
        menu.delete(0, "end")
        for option in new_options:
            menu.add_command(label=option, command=lambda value=option: self.on_option_select(value))
        if new_options:
            self.current_image_name.set(new_options[0])
            self.change_image(new_options[0])
        else:
            self.current_image_name.set("No images available")

    def on_option_select(self, value):
        self.current_image_name.set(value)
        self.option_changed()

    def set_text_data(self, data):
        beautified_json = json.dumps(data, indent=4)
        self.pretty_print_json(beautified_json)

    def start_ui(self):
        self.root.mainloop()

    def pretty_print_json(self, data):
        self.text_box.delete(1.0, 'end')

        def insert_with_tag(content, tag):
            self.text_box.insert('end', content, tag)

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

