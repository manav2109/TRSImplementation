# # Comparison of OCR
import os
import random
import re
import tempfile

import joblib
import pandas as pd

from routers.openai_module import check_part_number
from src.mvp_codelearn_dtree import extract_features, train_ml_model_for_airbus_part_numbers

temp_directory = tempfile.gettempdir()
print(f"temp_directory = {temp_directory}")
img_path = f"{temp_directory}/page7_image2.jpg"

import pytesseract
import cv2
#os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

#
# # Path to Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
# # Read the image using OpenCV
# image = cv2.imread(img_path)
#
#
# # Increase contrast and brightness
# alpha = 1.5  # Contrast control (1.0-3.0)
# beta = 50  # Brightness control (0-100)
#
# enhanced_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
# blurred = cv2.GaussianBlur(image, (0, 0), 1.0)
# sharpened = cv2.addWeighted(image, 1.0 + 1.5, blurred, -1.5, 0)
#
# # Display the original and enhanced images
# cv2.imshow('Original Image', image)
# cv2.imshow('Enhanced Image', enhanced_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # Convert the image to grayscale
# gray = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
#
# # Apply thresholding to preprocess the image
# _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#
# # Perform OCR using Tesseract
# text = pytesseract.image_to_string(thresh)
#
# # Print the extracted text
# print("Extracted Text:")
# print(text)


import cv2
import numpy as np


# def preprocess_image(image_path):
#     # Load image
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#
#     # Step 1: Denoising
#     img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
#
#     # Step 2: Thresholding
#     _, img_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     # Step 3: Noise Removal
#     kernel = np.ones((2, 2), np.uint8)
#     img_opening = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
#
#     # Step 4: Deskewing
#     # coords = np.column_stack(np.where(img_opening > 0))
#     # angle = cv2.minAreaRect(coords)[-1]
#     # if angle < -45:
#     #     angle = -(90 + angle)
#     # else:
#     #     angle = -angle
#     # (h, w) = img.shape[:2]
#     # center = (w // 2, h // 2)
#     # M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     # img_deskewed = cv2.warpAffine(img_opening, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#
#     # Step 5: Contrast Enhancement
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     img_clahe = clahe.apply(img_opening)
#
#     # Step 6: Binarization
#     _, img_bin = cv2.threshold(img_clahe, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     # Step 7: Resize
#     #img_resized = cv2.resize(img_bin, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
#
#     return img_bin
#
# # Example usage
# image_path = img_path
# preprocessed_image = preprocess_image(image_path)
# cv2.imshow("Preprocessed Image", preprocessed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # Perform OCR using Tesseract
# text = pytesseract.image_to_string(preprocessed_image)
#
# # Print the extracted text
# print("Extracted Text:")
#
# for i in range(0, 101):
#     random_4_number = random.randint(1000, 9999)
#     random_2_number = random.randint(1, 99)
#     VB = str(random_4_number) + 'VB ' + str(random_2_number) + 'M'
#     # print(VB)
#     random_11_number = random.randint(92000000000, 92899999999)
#     print('V'+str(random_11_number)+'-BS'+str(random_2_number))


# def has_spaces_or_special_characters(s):
#     # Regular expression to match any whitespace or special character
#     pattern = re.compile(r'[\s\W]')
#     # Search for the pattern in the string
#     if pattern.search(s):
#         return True
#     else:
#         return False
#
# def remove_special_characters(s):
#     # Regular expression to match any special character
#     pattern = re.compile(r'[^A-Za-z0-9\s\-]')
#     # Replace special characters with an empty string
#     clean_string = pattern.sub('', s)
#     return clean_string
#
# from autocorrect import Speller
#
# spell = Speller(lang='en')
#
# sample = ['Fret-MOD sketch:', 'Description', 'Post-MOD sketch:', 'E_a.E. — Cable Loom', 'inst. drawings — Modify', 'harnesses insta‘llatiun', 'tor DHSC in Dimr', 'Zone D3 LH FWD', '(eel. G}', 'Legend', 'Extremity Delta:', 'Pawn“: Extremity Status', 'I Existing', 'MOR - (9291mm not involved}', 'Addedtmoclmed', 'I', 'FzF (929mm involved}', 'Removed', 'Floor', "' —' (gzgtnltlllllwolvea)", '- CILATiWoIMed', 'A330 — Harness PreeLtetlnltlon', 'TOOTVCBAD—B _ _', 'on 88—00 plate _ ‘—', 'Flight Direction', 'mowcaameA', 'on BBAOD plate', "2563VB-1MDJ'1 MDE", '_"—b', '1?13VB -', '1MDF1MDEF1MTI1MTE', '700 Né640~C', 'Y0 19V0660 —A']

# def perform_spell_correction(sample):
#     # sample = ['Fret-MOD sketch:', 'Description', 'Post-MOD sketch:', 'E_a.E. — Cable Loom', 'inst. drawings — Modify', 'harnesses insta‘llatiun', 'tor DHSC in Dimr', 'Zone D3 LH FWD', '(eel. G}', 'Legend', 'Extremity Delta:', 'Pawn“: Extremity Status', 'I Existing', 'MOR - (9291mm not involved}', 'Addedtmoclmed', 'I', 'FzF (929mm involved}', 'Removed', 'Floor', "' —' (gzgtnltlllllwolvea)", '- CILATiWoIMed', 'A330 — Harness PreeLtetlnltlon', 'TOOTVCBAD—B _ _', 'on 88—00 plate _ ‘—', 'Flight Direction', 'mowcaameA', 'on BBAOD plate', "2563VB-1MDJ'1 MDE", '_"—b', '1?13VB -', '1MDF1MDEF1MTI1MTE', '700 Né640~C', 'Y0 19V0660 —A']
#     ret = []
#     for s in sample:
#         if has_spaces_or_special_characters(s):
#             # print(f"Need to treat {s}")
#             arr = s.split(' ')
#             dump = []
#             for a in arr:
#                 a = remove_special_characters(a)
#                 res = spell(a)
#                 if res != a:
#                     dump.append(res)
#                 else:
#                     dump.append(a)
#             fin = ' '.join(dump)
#             ret.append(fin)
#             #print(f"Original {s} change to {fin}")
#     return ret


#print(spell('installatiun'))
#print(spell('mussage'))
#print(spell('survice'))
#print(spell('hte'))


# import fitz  # For handling PDFs
# from pdf2image import convert_from_path  # For converting PDF to images
# import pytesseract  # For OCR
#
# def extract_pdf_data(pdf_path):
#   """
#   Extracts text and OCR data from a PDF file.
#
#   Args:
#       pdf_path: Path to the PDF file.
#
#   Returns:
#       A tuple containing:
#           - Text extracted from the PDF using PyMuPDF (may not work for scanned PDFs)
#           - OCR data extracted from images of the PDF pages using Tesseract OCR
#   """
#
#   # Open the PDF document
#   with fitz.open(pdf_path) as doc:
#     # Extract text using PyMuPDF (works for non-scanned PDFs)
#     pdf_text = ""
#     for page in doc:
#       pdf_text += page.get_text() + "\n"
#
#   # Convert PDF pages to images for OCR
#   images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
#
#   # Extract text from images using OCR (Tesseract)
#   ocr_text = ""
#   for image in images:
#     # Deskew the image if needed (implement deskewing function here)
#     # ocr_text += pytesseract.image_to_string(image, config='--psm 6') # Use page layout mode 6 for better results on multi-column PDFs
#     ocr_text += pytesseract.image_to_string(image)  # Basic OCR
#
#   return pdf_text, ocr_text
#
# # Example usage
# pdf_path = (r"C:\Users\abhij\PycharmProjects\TRSImplementation\TestData\SampleTRSSheets\GEN_Pdf_TRS_L26118_07082018_132507.pdf")
# text, ocr_data = extract_pdf_data(pdf_path)
#
# print("Text extracted from PDF (may not work for scanned PDFs):")
# print(text)
#
# print("\nOCR data extracted from images:")
# print(ocr_data)




#DT = train_my_model()
#new_strings = pd.Series(['V92373336527-BS70'])  # you can change and test against random set
#new_features = new_strings.apply(lambda x: pd.Series(extract_features(x)))
#predictions = DT.predict(new_features)
#predict_airbus_part_number(new_features)

# train_ml_model_for_airbus_part_numbers()

# # predict against new data
# new_strings = pd.Series(['8817VB 95M', 'W9296S000', 'V92369097810-BS99', 'V923690810-BS11']) #you can change and test against random set
# new_features = new_strings.apply(lambda x: pd.Series(extract_features(x)))
# new_pred = DT.predict(new_features)
# print(list(zip(new_strings, new_pred)))
# new_prob = DT.predict_proba(new_features)
# print(np.max(np.where(new_prob < 1, new_prob, np.nan), axis=1))

# check_part_number(['8817VB 95M', 'W9296S000', 'V92369097810-BS99', 'V923690810-BS11'])