import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def preprocess_image(image):
    resized_image = cv2.resize(image, (800, 600))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded_image


def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()
    return cleaned_text


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = {"Pre": [], "Post": []}

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_np = np.frombuffer(image_bytes, dtype=np.uint8)
            decoded_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            preprocessed_image = preprocess_image(decoded_image)
            extracted_text = pytesseract.image_to_string(preprocessed_image, lang="eng", config="--psm 6 --oem 3")
            cleaned_text = clean_text(extracted_text)

            if img_index == 0:
                text_data["Pre"].append(cleaned_text)
            elif img_index == 1:
                text_data["Post"].append(cleaned_text)

    doc.close()
    return text_data

