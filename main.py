import os
import pytesseract

from routers.nlp import get_purpose_of_the_sentence
from routers.ocr import single_image_to_json
from src.objects import tred_json
from src.pdf_extraction import read_pdf

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
    #for page in pdf_doc_obj.get_all_pages():
    #    page.page_text_analysis()


run_case = 1

if run_case == 1:
    trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
                                     'GEN_Pdf_TRS_L26118_07082018_132507.pdf')
elif run_case == 2:
    trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
                                     'GEN_Pdf_TRS_L25925_26092018_064958.pdf')
else:
    trs_pdf_file_path = os.path.join(os.getcwd(), 'TestData', 'SampleTRSSheets',
                                     'GEN_Pdf_SubTRS_L90032_XW CEF_30032018_064656.pdf')

extract_text_from_pdf(trs_pdf_file_path)
