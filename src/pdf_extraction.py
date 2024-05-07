import pdfplumber

import pdfplumber


def read_pdf(pdf_path):
    text_content = []
    table_content = []
    image_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from each page
            text_content.append(page.extract_text())

            # Extract tables from each page
            tables = page.extract_tables()
            table_content.extend(tables)

            # Extract images from each page
            images = page.images
            image_content.extend(images)

    return text_content, table_content, image_content


# Replace 'example.pdf' with the path to your PDF file
pdf_text, pdf_tables, pdf_images = read_pdf('example.pdf')

# Print text content
for page_num, text in enumerate(pdf_text, start=1):
    print(f"Page {page_num} Text:")
    print(text)
    print()

# Print table content
for table_num, table in enumerate(pdf_tables, start=1):
    print(f"Table {table_num}:")
    for row in table:
        print(row)
    print()

# Print image content
for image_num, image in enumerate(pdf_images, start=1):
    print(f"Image {image_num}:")
    print(image)
    print()
