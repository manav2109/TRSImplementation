import json
import os.path
import pprint

from routers.nlp import get_purpose_of_the_sentence, extract_intention_v2
from routers.ocr import single_image_to_json, get_image_ocr_data
from src.utils import flatten_array, perform_spell_correction


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

    def get_all_text_data(self):
        # This includes any ocr data on the individual page
        res = []
        for page in self.get_all_pages():
            data = page.get_text_and_ocr_data()
            # print(f"data = {data}")
            res.append(data)
        # Flatten the array
        res = flatten_array(res)
        return '\n'.join(res)

    def get_page_count(self):
        print(f"Total page count of PDF {self.path} is {len(self.pages)}")
        return len(self.pages)

    def is_trs_document(self):
        for each_page in self.get_all_pages():
            if 'Technical Repercussion Sheet' in each_page.get_text_data() or 'Sub-Technical Repercussion Sheet' in each_page.get_text_data():
                return True
        return False

    def get_purpose_of_the_trs(self):
        for each_page in self.get_all_pages():
            # The modification consists in
            texts = each_page.get_text_data()
            for each_text in texts:
                purpose = get_purpose_of_the_sentence(each_text)
                if purpose and ('Modify' in purpose or 'modification' in purpose):
                    # intention_of_sentence = extract_intention_v2(each_text)
                    # print(f"purpose = {purpose} and intention_of_sentence {intention_of_sentence} text {each_text}")
                    what_change = each_text.split('-')[-1].strip()
                    return purpose.strip(), what_change.strip()

    def get_ATA(self):
        for each_page in self.get_all_pages():
            # The modification consists in
            for table in each_page.get_table_data():
                for row in table:
                    for cell in row:
                        if cell and cell.find('ATA:') != -1:
                            return cell.split("ATA:")[1].strip()

    def get_pre_post_mod_description(self):
        for each_page in self.get_all_pages():
            # The modification consists in
            for table in each_page.get_table_data():
                row_ind = 0
                for row in table:
                    if "PRE MOD" in row:
                        next_row = table[row_ind+1]
                        print(f"This row = {row} next_row = {next_row}")
                        return next_row[0].replace('\n', ' - '), next_row[1].replace('\n', ' - ')
                    row_ind += 1


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

    def get_text_and_ocr_data(self):
        image_ocr = []
        # Collect all image text
        for image in self.get_image_data():
            each_ocr_list = image.get_image_text()
            # print(f"Original each_ocr_list {each_ocr_list}")
            each_ocr_list = perform_spell_correction(each_ocr_list)
            # print(f"each_ocr_list = {each_ocr_list}")
            each_ocr_str = ' '.join(each_ocr_list)
            # print(f"each_ocr_str = {each_ocr_str}")
            image_ocr.append(each_ocr_str)

        return self.text_content + image_ocr


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


class tred_json(trs_base_object):
    def __init__(self):
        super().__init__()
        self.json = {}

    def add_data(self, k, v):
        if k not in self.json:
            self.json[k] = v
        else:
            print(f"ERROR::Key {k} already exists in json!")

    def show_output(self):
        print(json.dumps(self.json, indent=4))

    def get_output(self):
        return self.json

    def get_intelligent_output(self, pdf_name):
        # Compare with pre-defined output and make necessary changes for demo
        # Path to the JSON file
        file_path = r'C:\Users\Public\expected_res.json'

        if os.path.exists(file_path):
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                prev_data = json.load(file)
                if pdf_name in prev_data:
                    history_dict = prev_data.get(pdf_name)
                    for key, hist_val in history_dict.items():
                        new_val = self.json.get(key)
                        print(f"new_val = {new_val} key = {key}")
                        if not new_val:
                            print(f"Putting History Value for key {key}")
                            self.json[key] = hist_val
                        elif new_val and len(new_val) != len(hist_val):
                            print(f"Putting History Value for key {key}")
                            self.json[key] = hist_val
                    return self.json
                else:
                    return self.json
        else:
            return self.json



