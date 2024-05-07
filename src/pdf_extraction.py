import pdfplumber
from src.objects import pdf_document
from src.objects import pdf_page


def read_pdf(pdf_path):
    # text_content = []
    # table_content = []
    # image_content = []

    with pdfplumber.open(pdf_path) as pdf:
        pdf_file_obj = pdf_document(pdf_path)

        page_count = 0
        for page in pdf.pages:
            page_count += 1
            pdf_page_obj = pdf_page(page)
            pdf_page_obj.set_page_number(page_count)

            # Extract text from each page
            pdf_page_obj.set_text_data(page.extract_text())
            # text_content.append(page.extract_text())

            # Extract tables from each page
            pdf_page_obj.set_table_data(page.extract_tables())
            # tables = page.extract_tables()
            # table_content.extend(tables)

            # Extract images from each page
            pdf_page_obj.set_image_data(page.images)
            # images = page.images
            # image_content.extend(images)

            # Add page to doc
            pdf_file_obj.add_page(pdf_page_obj)

    return pdf_file_obj


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
