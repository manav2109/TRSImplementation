import os
import pdfplumber
from openai import OpenAI
from src.objects import tred_json, pdf_document
from src.pdf_extraction import read_pdf


def chat_with_gpt(pdf_text, seed):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # prompt = f"Q: {question}\nContext: {pdf_text}"
    # response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150)

    # To ensure that the OpenAI client.chat.completions.create method gives
    # consistent answers for the same input data, you need to set the seed parameter in the request.The seed
    # parameter specifies a random seed value that controls the randomization process used by the model.Providing the
    # same seed value for the same input data ensures deterministic behavior, resulting in consistent responses.
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
                "content": "Get following information from the data provided:"
                           "Purpose:"
                           "Reason:"
                           "Modification:"
                           "Aircraft Name:"
                           "Before Change:"
                           "After Change:"
                           "Proposed Change:"
                           "Impact Assessment:"
                           "Impact on or Impacts on:"
                           "Repercussions:"
                           "ATA:"
                           "Pre Mod or Pre-Mod or Pre Modification or Pre-Modification:"
                           "Post Mod or Post-Mod or Post Modification or Post-Modification:"
                           "Changes in quantity of clamps, nuts & other loose items:"
                           "VB with suffix and prefix:"
                           "Part Numbers in comma separated format:",
            },

        ],
        max_tokens=700,  # Increase if you need a more detailed response
        temperature=0.7,  # Adjust for creativity in response; lower for more factual
        seed=seed
    )

    return response.choices[0].message.content
    # response.choices[0].text.strip()
    # return response.json()


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


def string_to_integer_sum_alphabet(string):
    string = string.upper()  # Convert string to uppercase for consistency
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    total = ''
    for char in string:
        # 9223372036854775807
        if len(total) > 18:
            continue
        if char.isalpha():  # Check if the character is an alphabet
            position = alphabet.index(char) + 1  # Get the position of the alphabet
            total += str(position)
        elif char.isdigit():
            total += str(char)
    return int(total)


def get_gpt_extract(pdf_path):
    # pdf_text = extract_text_from_pdf(pdf_path)
    pdf_doc = read_pdf(pdf_path)
    pdf_text = pdf_doc.get_all_text_data()
    # print(f"pdf_text = {pdf_text}")

    # To ensure that the OpenAI client.chat.completions.create method gives
    # consistent answers for the same input data, you need to set the seed parameter in the request.The seed
    # parameter specifies a random seed value that controls the randomization process used by the model.Providing the
    # same seed value for the same input data ensures deterministic behavior, resulting in consistent responses.
    seed_val = string_to_integer_sum_alphabet(os.path.basename(pdf_path))
    print(f"seed val is {seed_val} for file {os.path.basename(pdf_path)}")
    gpt_extract = chat_with_gpt(pdf_text, seed_val)
    print(f"gpt_extract = {gpt_extract}")
    gpt_extract_as_arr = gpt_extract.split('\n')

    output = tred_json()
    for each_line in gpt_extract_as_arr:
        in_arr = each_line.split(':')
        if len(in_arr) > 1:
            key = in_arr[0].strip()
            val = in_arr[1].strip()

            if (key == 'Part Numbers in comma separated format' or key == 'VB Numbers' or
                    key == 'Changes in quantity of clamps, nuts & other loose items'):
                if key == 'Part Numbers in comma separated format':
                    key = 'Affected Part Numbers'
                elif key == 'VB with suffix and prefix':
                    key = 'Affected VBs'
                elif key == 'Changes in quantity of clamps, nuts & other loose items':
                    key = 'Quantity Changes'

                split_val = val.split(',')
                output.add_data(key, split_val)
            else:
                output.add_data(key, val)
        else:
            print(f"WARNING::Line {each_line} can not be split!")

    return output

    # extract_path = r'C:\Users\abhij\PycharmProjects\TRSImplementation\TestData\SampleTRSSheets\gpt_feed_1.txt'
    # split_tags = ['Purpose:', 'Situation before modification:', 'Situation after modification:']
    # gpt_extract = read_file_as_string(extract_path)
    # print(f"file_content = {file_content}")

    # tag_count = 0
    # output = tred_json()
    # for each_tag in split_tags:
    #     if tag_count < len(split_tags) - 1:
    #         next_tag = split_tags[tag_count + 1]
    #         res = split_string_by_endpoints(gpt_extract, each_tag, next_tag)
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
