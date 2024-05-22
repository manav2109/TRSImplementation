import io
import tempfile

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageEnhance
from PIL.Image import Resampling

from utils.utils import transform_image_to_text


def single_image_to_json(image_file_path):
    image = Image.open(image_file_path)
    text = transform_image_to_text(image)
    return [line.strip() for line in text.split('\n') if line.strip()]


def get_image_ocr_data(image_object):
    # image_object is individual image retrieved using method pdf_fitz_utility->get_pdf_page_images() which is put
    # in class pdf_image
    image_ind = image_object.original_image_data[0]
    base_image = image_object.fitz_doc_obj.extract_image(image_ind)

    # Get image data
    image_bytes = base_image["image"]

    # Convert image data to PIL Image
    image = Image.open(io.BytesIO(image_bytes))

    # Get original width and height
    original_width, original_height = image.size

    # Calculate new width and height
    new_width = int(original_width * 2.0)
    new_height = int(original_height * 2.0)
    #
    # # Resize the image
    image = image.resize((new_width, new_height), resample=Resampling.BOX)
    # factor = min(1, float(1024.0 / original_width))
    # size = int(factor * original_width), int(factor * original_height)
    # image = image.resize(size, Resampling. NEAREST)

    # Enhance brightness
    brightness_factor = 1.2
    sharpness_factor = 1.5
    contrast_factor = 1.2
    # enhancer = ImageEnhance.Brightness(image)
    # image = enhancer.enhance(brightness_factor)

    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness_factor)

    # Enhance contrast
    # enhancer = ImageEnhance.Contrast(image)
    # image = enhancer.enhance(contrast_factor)

    # Save the image as JPG
    temp_directory = tempfile.gettempdir()
    img_path = f"{temp_directory}/page{image_object.page_number}_image{image_object.image_index}.jpg"
    image.save(img_path, dpi=(300, 300))
    # print(f"img_path = {img_path}")
    image.close()

    # Get OCR data
    # img_path = image_enhancement_for_ocr(image_object)
    ocr_text_data = single_image_to_json(img_path)
    # print(f"ocr_text_data = {ocr_text_data}")
    return ocr_text_data


def set_image_dpi(file_path):
    img = Image.open(file_path)
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = img.resize(size, Resampling.NEAREST)
    # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=’.png’)
    # temp_filename = temp_file.name
    im_resized.save(file_path, dpi=(300, 300))
    return file_path


def image_enhancement_for_ocr(image_object):
    # Follow up at https://nextgeninvent.com/blogs/7-steps-of-image-pre-processing-to-improve-ocr-using-python-2/
    image_ind = image_object.original_image_data[0]
    base_image = image_object.fitz_doc_obj.extract_image(image_ind)

    # Get image data
    image_bytes = base_image["image"]

    # Convert image data to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    # Convert image data to PIL Image
    # Save the image as JPG
    temp_directory = tempfile.gettempdir()
    img_path = f"{temp_directory}/page{image_object.page_number}_image{image_object.image_index}.jpg"
    image.save(img_path)
    image.close()

    img = cv2.imread(img_path, 0)
    # 1. Normalisation
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    col = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

    col = cv2.threshold(col, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    col.dump(img_path)
    return img_path


def snap_of_image(self):
    # Get the page
    image_ind = self.original_image_data[0]
    base_image = self.fitz_doc_obj.extract_image(image_ind)
    print(f"base_image = {base_image}")
    #rect = base_image["rect"]
    image_region = (self.original_image_data[1],
                    self.original_image_data[2],
                    self.original_image_data[3],
                    self.original_image_data[4])  #(rect[0], rect[1], rect[2], rect[3])

    # Get the image region coordinates
    #print(f"self.original_image_data = {self.original_image_data}")
    x1, y1, x2, y2 = image_region

    # Calculate the position and size of the image region
    left, top = x1, y1  # self.original_page_object.rect.x0 + x1, self.original_page_object.rect.y1 - y1
    width, height = base_image['width'], base_image['height']  #x2 - x1, y1 - y2  # y-axis is inverted in PyMuPDF

    # Take a screenshot of the image region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # Save the screenshot
    temp_directory = tempfile.gettempdir()
    img_path = f"{temp_directory}/page{self.page_number}_snap_image{self.image_index}.jpg"
    screenshot.save(img_path)
