import pdfplumber
import re

# Open the PDF file
input_pdf = "C:/Users/manav/OneDrive/Desktop/TRSImplementation/TRS.pdf"
with pdfplumber.open(input_pdf) as pdf:
    document_info = dict()

    # Extract text from each page
    for i, page in enumerate(pdf.pages):
        word_bboxes = []
        words = page.extract_words()
        for word in words:
            text = word["text"]
            bbox = [word["x0"], word["top"], word["x1"], word["bottom"]]
            word_bboxes.append({"text": text, "bbox": bbox})

        document_info[i] = {"document": word_bboxes, "dimension": [page.width, page.height]}

# Use regular expression to find key-value pairs
pattern = re.compile(r'(.*?):\s(.*?)\s')
key_value_pairs = dict()
for page_num, page_info in document_info.items():
    for word_info in page_info["document"]:
        match = re.match(pattern, word_info["text"])
        if match:
            key, value = match.groups()
            key_value_pairs[key] = value

# Print the extracted key-value pairs
for key, value in key_value_pairs.items():
    print(f"{key}: {value}")
