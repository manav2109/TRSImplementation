import os
import pytesseract

from routers.nlp import get_purpose_of_the_sentence
from routers.ocr import single_image_to_json
from src.pdf_extraction import read_pdf

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def extract_text_from_pdf(pdf_path):
    pdf_doc_obj = read_pdf(pdf_path)
    pdf_doc_obj.get_page_count()
    print(f"is_trs_document = {pdf_doc_obj.is_trs_document()}")
    print(f"get_purpose_of_the_trs = {pdf_doc_obj.get_purpose_of_the_trs()}")

    # Loop through each page
    # for page in pdf_doc_obj.get_all_pages():
    #     page.page_image_analysis()


trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets', 'GEN_Pdf_TRS_L26118_07082018_132507.pdf')
extract_text_from_pdf(trs_pdf_file_path)


