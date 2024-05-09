import pprint

from routers.nlp import get_purpose_of_the_sentence, extract_intention_v2
from routers.ocr import single_image_to_json, get_image_ocr_data


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

    def is_trs_document(self):
        for each_page in self.get_all_pages():
            if 'Technical Repercussion Sheet' in each_page.get_text_data():
                return True
        return False

    def get_purpose_of_the_trs(self):
        for each_page in self.get_all_pages():
            # The modification consists in
            texts = each_page.get_text_data()
            for each_text in texts:
                purpose = get_purpose_of_the_sentence(each_text)
                if purpose and ('Modify' in purpose or 'modification' in purpose):
                    # intension_of_sentence = extract_intention_v2(each_text)
                    # print(f"purpose = {purpose} and intension_of_sentence {intension_of_sentence} text {each_text}")
                    what_change = each_text.split('-')[-1].strip()
                    return purpose.strip(), what_change.strip()


class pdf_page(trs_base_object):
    def __init__(self, original_page_object):
        super().__init__()
        self.original_page_object = original_page_object
        self.number_of_images = None
        self.text_content = []
        self.table_content = []
        self.image_content = []
        self.image_objects_list = []
        self.page_number = None

    def set_text_data(self, text_data):
        # Array data of all texts on the page
        self.text_content = text_data.split('\n')

    def set_table_data(self, table_data):
        self.table_content = table_data

    def set_image_data(self, image_data, fitz_doc_obj, fitz_page):
        self.number_of_images = len(image_data)
        self.image_content = image_data
        image_index = 0
        for individual_image in image_data:
            image_index += 1
            img_obj = pdf_image(individual_image, self.original_page_object, self.page_number, fitz_doc_obj,
                                image_index, fitz_page)
            self.image_objects_list.append(img_obj)

    def set_page_number(self, num):
        self.page_number = num

    def get_text_data(self):
        # Returns array of strings consisting all texts on this page
        return self.text_content

    def get_table_data(self):
        return self.table_content

    def get_image_data(self):
        return self.image_objects_list

    def get_page_number(self):
        return self.page_number

    def print_page_data_status(self):
        print(f"Page {self.get_page_number()} have:\n----------------------------------")
        print(f"total text_contents are: {len(self.text_content)}")
        print(f"total number of images are: {self.number_of_images}")
        print(f"total number of tables are {len(self.table_content)}")
        print(f"----------------------------------")

    def page_text_analysis(self):
        # for text in self.text_content:
        print(f"Page Number {self.page_number} Each text = {self.text_content}")

    def page_table_analysis(self):
        for table in self.table_content:
            print(f"Page Number {self.page_number} Each table = {table}")

    def page_image_analysis(self):
        for image in self.get_image_data():
            print(f"Page Number {image.page_number}. Each image = {image} Text = {image.get_image_text()}")


class pdf_image(trs_base_object):
    def __init__(self, individual_image, original_page_object, page_number, fitz_doc_obj, image_index, fitz_page):
        super().__init__()
        self.original_image_data = individual_image
        self.original_page_object = original_page_object
        self.page_number = page_number
        self.fitz_doc_obj = fitz_doc_obj
        self.image_index = image_index
        self.fitz_page = fitz_page

    def get_image_text(self):
        ocr_text_data = get_image_ocr_data(self)
        return ocr_text_data

    # def get_image_text(self):
    #     xref = self.original_image_data[0]
    #     base_image = self.fitz_doc_obj.extract_image(xref)
    #     image_bytes = base_image["image"]
    #     image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    #     decoded_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    #     preprocessed_image = self.preprocess_image(decoded_image)
    #     extracted_text = pytesseract.image_to_string(preprocessed_image, lang="eng", config="--psm 6 --oem 3")
    #     cleaned_text = self.clean_text(extracted_text)
    #     # print(f"{self.page_number+1}. extracted_text = {extracted_text}")
    #     return cleaned_text

    # def preprocess_image(self, image):
    #     resized_image = cv2.resize(image, (800, 600))
    #     gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    #     _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #     return thresholded_image
    #
    # def clean_text(self, text):
    #     # print(f"Before Cleaning {text}")
    #     cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()
    #     return cleaned_text


