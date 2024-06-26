import os

import fitz
import pdfplumber
import pytesseract

from src.objects import pdf_document, tred_json
from src.objects import pdf_page

page_categories = {
    "GEN_Pdf_TRS_L26118_07082018_132507.pdf": {
        "Introduction": [1],
        "Authors": [2],
        "General Description": [3, 4, 5],
        "Changes": [6, 7, 8],
        "Repercussions": [10, 11],
        "Part Numbers": [12, 13]
    },
    "GEN_Pdf_TRS_L25925_26092018_064958.pdf": {
        "Introduction": [1],
        "Authors": [2],
        "General Description": [3, 4],
        "Changes": [5, 6, 7, 8, 9],
        "Repercussions": [10, 11],
        "Part Numbers": [12, 13]
    },
    "GEN_Pdf_SubTRS_L90032_XW CEF_30032018_064656.pdf": {
        "Introduction": [1],
        "Authors": [2],
        "General Description": [3, 4, 5],
        "Changes": [6, 7, 8, 9, 10, 11],
        "Repercussions": [13, 14],
        "Part Numbers": [15, 16]
    },
}


def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pdf_name = os.path.basename(pdf_path)
        pdf_file_obj = pdf_document(pdf_path)
        pdf_fitz_utility_obj = pdf_fitz_utility(pdf_path)

        page_count = 0
        for page in pdf.pages:
            page_count += 1
            pdf_page_obj = pdf_page(page, pdf_name)
            pdf_page_obj.set_page_number(page_count)
            # Set page category. Hard coded for certain files for now
            pdf_page_obj.set_page_category(pdf_name, page_categories)

            # Extract text from each page
            pdf_page_obj.set_text_data(page.extract_text())
            # text_content.append(page.extract_text())

            # Extract tables from each page
            pdf_page_obj.set_table_data(page.extract_tables())
            # tables = page.extract_tables()
            # table_content.extend(tables)

            # Extract images from each page
            # pdf_page_obj.set_image_data(page.images)
            image_data, fitz_page = pdf_fitz_utility_obj.get_pdf_page_images(page_count)
            # print(f"image_data = {image_data}")
            pdf_page_obj.set_image_data(image_data, pdf_fitz_utility_obj.get_fitz_doc(), fitz_page)

            if len(image_data) != len(page.images):
                print(f"ERROR::Image count on page {page_count} is not matching...{len(image_data), len(page.images)}")
            # images = page.images
            # image_content.extend(images)

            # Add page to doc
            pdf_file_obj.add_page(pdf_page_obj)

    return pdf_file_obj


# Get all image information using fitz package as pytesseract which does the OCR works with it only
class pdf_fitz_utility(object):
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)

    def get_pdf_page_images(self, page_number):
        # page_number supplied is starting from 1, so we have to lessen it by 1
        for page_num in range(self.doc.page_count):
            if page_num == page_number - 1:
                page = self.doc.load_page(page_num)
                image_list = page.get_images(full=True)
                return image_list, page

    def get_fitz_doc(self):
        return self.doc

    # text_data = {"Pre": [], "Post": []}
    #
    # for page_num in range(doc.page_count):
    #     page = doc.load_page(page_num)
    #     image_list = page.get_images(full=True)
    #     #print(f"image_list = {image_list}")
    #
    #     for img_index, img in enumerate(image_list):
    #         #print(f"img = {img[0]}")
    #         xref = img[0]
    #         base_image = doc.extract_image(xref)
    #         image_bytes = base_image["image"]
    #         image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    #         decoded_image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    #         preprocessed_image = preprocess_image(decoded_image)
    #         extracted_text = pytesseract.image_to_string(preprocessed_image, lang="eng", config="--psm 6 --oem 3")
    #         cleaned_text = clean_text(extracted_text)
    #         print(f"{page_num+1}. extracted_text = {extracted_text}")


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def extract_text_from_pdf(pdf_path):
    pdf_doc_obj = read_pdf(pdf_path)
    pdf_doc_obj.get_page_count()
    # print(f"is_trs_document = {pdf_doc_obj.is_trs_document()}")
    purpose, change = pdf_doc_obj.get_purpose_of_the_trs()
    ata = pdf_doc_obj.get_ATA()
    pre_mod, post_mod = pdf_doc_obj.get_pre_post_mod_description()
    # print(f"get_purpose_of_the_trs = {pdf_doc_obj.get_purpose_of_the_trs()}")

    output = tred_json()
    output.add_data('is_trs_document', pdf_doc_obj.is_trs_document())
    output.add_data('purpose', purpose)
    output.add_data('change', change)
    output.add_data('ata_chapter', ata)
    output.add_data('pre_mod_description', pre_mod)
    output.add_data('post_mod_description', post_mod)
    output.add_data('CI', "")
    output.add_data('DS', "")
    output.add_data('ZONE', "")
    output.add_data('part_number', "")
    updates_dict = {"part_number": "",
                    "current_co-ordinates_in_ac": [],
                    "new_co-ordinates_in_ac": [],
                    "feature_name": "",
                    "feature_parameter": "",
                    "feature_dim": ""}
    output.add_data('updates', updates_dict)
    print(f"output = {output.show_output()}")

    # Loop through each page
    # for page in pdf_doc_obj.get_all_pages():
    #     page.page_image_analysis()

    return output

# run_case = 1
#
# if run_case == 1:
#     trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
#                                      'GEN_Pdf_TRS_L26118_07082018_132507.pdf')
# elif run_case == 2:
#     trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
#                                      'GEN_Pdf_TRS_L25925_26092018_064958.pdf')
# else:
#     trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
#                                      'GEN_Pdf_SubTRS_L90032_XW CEF_30032018_064656.pdf')
#
# extract_text_from_pdf(trs_pdf_file_path)

# def preprocess_image(image):
#     resized_image = cv2.resize(image, (800, 600))
#     gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
#     _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return thresholded_image
#
#
# def clean_text(text):
#     #print(f"Before Cleaning {text}")
#     cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()
#     return cleaned_text

# # Replace 'example.pdf' with the path to your PDF file
# pdf_text, pdf_tables, pdf_images = read_pdf('example.pdf')
#
# # Print text content
# for page_num, text in enumerate(pdf_text, start=1):
#     print(f"Page {page_num} Text:")
#     print(text)
#     print()
#
# # Print table content
# for table_num, table in enumerate(pdf_tables, start=1):
#     print(f"Table {table_num}:")
#     for row in table:
#         print(row)
#     print()
#
# # Print image content
# for image_num, image in enumerate(pdf_images, start=1):
#     print(f"Image {image_num}:")
#     print(image)
#     print()
