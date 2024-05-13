#from openai import OpenAI
import pdfplumber
#client = OpenAI(api_key='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')

from openai import OpenAI

from src.objects import tred_json

client = OpenAI(api_key='sk-proj-ydulqKFdkR3u5rBhGhfjT3BlbkFJNfnkn592uDsHJaBdZbb6')


# Set your OpenAI API key

def chat_with_gpt(question, pdf_text):
    prompt = f"Q: {question}\nContext: {pdf_text}"
    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()


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
    print(f"XXXXXXXXx {string.count(":")} == {string.count("\n")}")
    return string.count(":") == string.count("\n") + 1 and ":" in string and "\n" in string


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


# def generate_response(question, pdf_text):
#     prompt = f"Q: {question}\nContext: {pdf_text}"
#     response = openai.Completion.create(
#         engine="text-davinci-002",  # Choose the appropriate model
#         prompt=prompt,
#         max_tokens=150,  # Adjust as needed
#     )


def get_gpt_extract(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    gpt_extract = chat_with_gpt("What is the main purpose of the document?", pdf_text)
    print(f"gpt_extract = {gpt_extract}")

    # extract_path = r'C:\Users\abhij\PycharmProjects\TRSImplementation\TestData\SampleTRSSheets\gpt_feed_1.txt'
    # split_tags = ['Purpose', 'Description Before and After Modification', 'Before Modification:', 'After Modification:',
    #               'Impact Assessment', 'This summary provides']
    # file_content = read_file_as_string(extract_path)
    # # print(f"file_content = {file_content}")
    #
    # tag_count = 0
    # output = tred_json()
    # for each_tag in split_tags:
    #     if tag_count < len(split_tags) - 1:
    #         next_tag = split_tags[tag_count + 1]
    #         res = split_string_by_endpoints(file_content, each_tag, next_tag)
    #         print(f"res = {res}")
    #         if res:
    #             if contains_colon_and_newline_with_same_count(res):
    #                 arr = res.split('\n')
    #                 dict = {}
    #                 for each_line in arr:
    #                     in_arr = each_line.split(':')
    #                     dict[in_arr[0].strip()] = in_arr[1].strip()
    #                 output.add_data(each_tag, dict)
    #             else:
    #                 output.add_data(each_tag, res)
    #     tag_count += 1
    #
    # return output
