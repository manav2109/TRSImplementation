import pprint


class trs_base_object(object):
    def __init__(self):
        pass

    def print(self):
        # Pretty print the object as a string
        formatted_object = pprint.pformat(self)
        print(formatted_object)
        # pprint.pprint(self)


class pdf_document(trs_base_object):
    def __init__(self, pdf_path):
        super().__init__()
        self.doc = None
        self.pages = []
        self.path = pdf_path

    def set_document(self, doc):
        self.doc = doc

    def get_document(self):
        return self.doc

    def set_pages(self, pages):
        self.pages = pages

    def add_page(self, page):
        self.pages.append(page)

    def get_all_pages(self):
        return self.pages

    def get_page_count(self):
        print(f"Total page count of PDF {self.path} is {len(self.pages)}")
        return len(self.pages)


class pdf_page(trs_base_object):
    def __init__(self):
        super().__init__()
        self.number_of_images = None
        self.text_content = []
        self.table_content = []
        self.image_content = []
        self.page_number = None

    def set_text_data(self, text_data):
        self.text_content = text_data

    def set_table_data(self, table_data):
        self.table_content = table_data

    def set_image_data(self, image_data):
        self.number_of_images = len(image_data)
        self.image_content = image_data

    def set_page_number(self, num):
        self.page_number = num

    def get_text_data(self):
        return self.text_content

    def get_table_data(self):
        return self.table_content

    def get_image_data(self):
        return self.image_content

    def get_page_number(self):
        return self.page_number

    def print_page_data_status(self):
        print(f"Page {self.get_page_number()} have:\n----------------------------------")
        print(f"total text_contents are: {len(self.text_content)}")
        print(f"total number of images are: {self.number_of_images}")
        print(f"total number of tables are {len(self.table_content)}")
        print(f"----------------------------------")

    def table_analysis(self):
        for table in self.table_content:
            print(f"Each table = {table}")

    def image_analysis(self):
        for image in self.get_image_data():
            print(f"{self.get_page_number()} Each image = {image}")

