import os
import pdfplumber
from openai import OpenAI
from src.objects import tred_json


def chat_with_gpt(pdf_text):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # prompt = f"Q: {question}\nContext: {pdf_text}"
    # response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150)
    response = client.chat.completions.create(
        model="gpt-4",  # Model name, best output

        messages=[
            {
                "role": "user",
                "content": pdf_text,  # specify the source
            },
            {
                "engine": "davinci",  # LLM engine, others can be used but this provides great output
                "role": "user",
                "content": "Can you summarize the purpose of this document, specify change and the ATA reference, "
                           "description before and after modifications, impact assessment find part numbers",
            },

        ],
        max_tokens=700,  # Increase if you need a more detailed response
        temperature=0.7  # Adjust for creativity in response; lower for more factual
    )

    return response.choices[0].message.content
    # response.choices[0].text.strip()


# Example usage:
# prompt = "Q: What is the meaning of life?"
# response = chat_with_gpt(prompt)
# print("A:", response)


def read_file_as_string(filepath):
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return None


def split_string_by_endpoints(input_string, start_point, end_point):
    print(f"Getting string between {start_point, end_point}")
    start_index = input_string.find(start_point)
    if start_index == -1:
        return None  # Start point not found
    end_index = input_string.find(end_point, start_index + len(start_point))
    if end_index == -1:
        return None  # End point not found after start point
    return input_string[start_index + len(start_point):end_index].strip()


def contains_colon_and_newline_with_same_count(string):
    return string.count(":") == string.count("\n") + 1 and ":" in string and "\n" in string


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def get_gpt_extract(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    # print(f"pdf_text = {pdf_text}")
    gpt_extract = chat_with_gpt(pdf_text)
    print(f"gpt_extract = {gpt_extract}")

    # extract_path = r'C:\Users\abhij\PycharmProjects\TRSImplementation\TestData\SampleTRSSheets\gpt_feed_1.txt'
    split_tags = ['Purpose:', 'Situation before modification:', 'Situation after modification:']
    # gpt_extract = read_file_as_string(extract_path)
    # print(f"file_content = {file_content}")

    tag_count = 0
    output = tred_json()
    for each_tag in split_tags:
        if tag_count < len(split_tags) - 1:
            next_tag = split_tags[tag_count + 1]
            res = split_string_by_endpoints(gpt_extract, each_tag, next_tag)
            print(f"res = {res}")
            if res:
                if contains_colon_and_newline_with_same_count(res):
                    arr = res.split('\n')
                    dict = {}
                    for each_line in arr:
                        in_arr = each_line.split(':')
                        dict[in_arr[0].strip()] = in_arr[1].strip()
                    output.add_data(each_tag, dict)
                else:
                    output.add_data(each_tag, res)
        tag_count += 1

    return output
