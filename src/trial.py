# # Comparison of OCR
import os
import random
import tempfile

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

for i in range(0, 101):
    random_4_number = random.randint(1000, 9999)
    random_2_number = random.randint(1, 99)
    VB = str(random_4_number) + 'VB ' + str(random_2_number) + 'M'
    # print(VB)
    random_11_number = random.randint(92000000000, 92899999999)
    print('V'+str(random_11_number)+'-BS'+str(random_2_number))
