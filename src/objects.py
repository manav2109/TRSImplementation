import io
import pprint
import re
import tempfile

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance
from PIL.Image import Resampling

from routers.ocr import single_image_to_json


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
            #image.snap_of_image()
            print(f"Page Number {image.page_number}. Each image = {image} Text = {image.get_image_text()}")

import pyautogui
class pdf_image(trs_base_object):
    def __init__(self, individual_image, original_page_object, page_number, fitz_doc_obj, image_index, fitz_page):
        super().__init__()
        self.original_image_data = individual_image
        self.original_page_object = original_page_object
        self.page_number = page_number
        self.fitz_doc_obj = fitz_doc_obj
        self.image_index = image_index
        self.fitz_page = fitz_page

    def snap_of_image(self):
        # Get the page
        image_ind = self.original_image_data[0]
        base_image = self.fitz_doc_obj.extract_image(image_ind)
        print(f"base_image = {base_image}")
        #rect = base_image["rect"]
        image_region = (self.original_image_data[1],
                        self.original_image_data[2],
                        self.original_image_data[3],
                        self.original_image_data[4]) #(rect[0], rect[1], rect[2], rect[3])

        # Get the image region coordinates
        #print(f"self.original_image_data = {self.original_image_data}")
        x1, y1, x2, y2 = image_region

        # Calculate the position and size of the image region
        left, top = x1, y1 # self.original_page_object.rect.x0 + x1, self.original_page_object.rect.y1 - y1
        width, height = base_image['width'], base_image['height']#x2 - x1, y1 - y2  # y-axis is inverted in PyMuPDF

        # Take a screenshot of the image region
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # Save the screenshot
        temp_directory = tempfile.gettempdir()
        img_path = f"{temp_directory}/page{self.page_number}_snap_image{self.image_index}.jpg"
        screenshot.save(img_path)

    def get_image_text(self, save_images=False):
        image_ind = self.original_image_data[0]
        base_image = self.fitz_doc_obj.extract_image(image_ind)

        # Get image data
        image_bytes = base_image["image"]

        # Convert image data to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Get original width and height
        original_width, original_height = image.size

        # Calculate new width and height
        new_width = int(original_width * 2.0)
        new_height = int(original_height * 2.0)

        # Resize the image
        image = image.resize((new_width, new_height), resample=Resampling.BOX)

        # Enhance brightness
        brightness_factor = 1.2
        sharpness_factor = 1.5
        contrast_factor = 1.2
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness_factor)

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness_factor)

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)

        # Save the image as JPG
        temp_directory = tempfile.gettempdir()
        img_path = f"{temp_directory}/page{self.page_number}_image{self.image_index}.jpg"
        image.save(img_path)

        # Get OCR data
        ocr_text_data = single_image_to_json(image,img_path)
        # print(f"data = {data}")

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
