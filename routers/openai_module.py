import math
import os
import statistics

import pdfplumber
from openai import OpenAI

from src.mvp_codelearn_dtree import train_ml_model_for_airbus_part_numbers, predict_airbus_part_number
from src.objects import tred_json, pdf_document
from src.pdf_extraction import read_pdf

USE_GPT_FLAG = True


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
                           "Changes in quantity:"
                           "VB with suffix and prefix:"
                           "Part Numbers in comma separated format:",
            },

        ],
        max_tokens=700,  # Increase if you need a more detailed response
        temperature=0.7,  # Adjust for creativity in response; lower for more factual
        seed=seed
    )

    return response.choices[0].message.content


def get_prompt_content_for_category(category):
    # "Introduction", "Authors", "General Description", "Changes", "Repercussions", "Part Numbers"
    if category == "Introduction":
        return "Get Introduction text from supplied data"
    elif category == "Authors":
        return "Get Authors Information from supplied data"
    elif category == "General Description":
        return "Get General Description from supplied data"
    elif category == "Changes":
        return "Get changes or modification information from supplied data"
    elif category == "Repercussions":
        return "Get Repercussion information from supplied data. Return results data in key and value format."
    elif category == "Part Numbers":
        return ("Get below information from supplied data."
                "Part Numbers:"
                "VB numbers with suffix and prefix:")


def chat_with_gpt_based_on_category(pdf_text, seed, category):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

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
                "content": get_prompt_content_for_category(category),
            },

        ],
        max_tokens=700,  # Increase if you need a more detailed response
        temperature=0.7,  # Adjust for creativity in response; lower for more factual
        seed=seed
    )

    return response.choices[0].message.content


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


def check_part_number(part_number_array):
    current_directory = os.getcwd()
    model_path = os.path.join(current_directory, "routers", "decision_tree_model.joblib")

    if not os.path.exists(model_path):
        # Trained ML model is not yet created so create it
        print(f"Creating and training ML model with supervised learning...")
        train_ml_model_for_airbus_part_numbers()

    # print(f"part_number_array = {part_number_array}")
    predictions = predict_airbus_part_number(part_number_array)

    res = statistics.fmean(predictions)
    print(f"part number prediction = {res}")
    if res > 0.6 or math.isnan(res):
        return True
    else:
        return False


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
    # print(f"seed val is {seed_val} for file {os.path.basename(pdf_path)}")

    # Set the Image Data
    image_ocr_objects = []
    for each_page in pdf_doc.get_all_pages():
        images = each_page.get_image_data()
        for each_image in images:
            # print(f"each_image = {each_image.get_image_name()} ocr_object = {each_image.ocr_object}")
            # img_path = each_image.ocr_object.get_image_with_ocr_boxes()
            image_ocr_objects.append(each_image.ocr_object)

    #return {}, image_ocr_objects

    if USE_GPT_FLAG:
        gpt_extract = chat_with_gpt(pdf_text, seed_val)
        print(f"gpt_extract = {gpt_extract}")
        gpt_extract_as_arr = gpt_extract.split('\n')

        output = tred_json()
        for each_line in gpt_extract_as_arr:
            in_arr = each_line.split(':')
            if len(in_arr) > 1:
                key = in_arr[0].strip()
                val = in_arr[1].strip()
                split_val = val.split(',')
                split_val = [s.strip() for s in split_val]

                if (key == 'Part Numbers in comma separated format' or key == 'VB with suffix and prefix' or
                        key == 'Changes in quantity'):
                    if key == 'Part Numbers in comma separated format':
                        key = 'Affected Part Numbers'
                        # print(f"Part numbers == {split_val}")
                        is_valid_part_numbers = check_part_number(split_val)
                        if is_valid_part_numbers:
                            print(f"All Airbus Part numbers are valid!!!!!!!!!!")
                            output.add_data(key, split_val)
                        else:
                            print(f"Invalid Airbus part numbers in {split_val}")
                    elif key == 'VB with suffix and prefix':
                        key = 'Affected VBs'
                        # print(f"Affected VBs == {split_val}")
                        is_valid_part_numbers = check_part_number(split_val)
                        if is_valid_part_numbers:
                            print(f"All Airbus Part numbers are valid!!!!!!!!!!")
                            output.add_data(key, split_val)
                        else:
                            print(f"Invalid Airbus part numbers in {split_val}")
                    elif key == 'Changes in quantity':
                        key = 'Quantitative Changes'
                        output.add_data(key, split_val)
                else:
                    output.add_data(key, val)
            elif each_line:
                print(f"WARNING::Line {each_line} can not be split!")

        return output.get_intelligent_output(os.path.basename(pdf_path)), image_ocr_objects
    else:
        return {}, image_ocr_objects



def get_category_based_gpt_extract(pdf_path):
    pdf_doc = read_pdf(pdf_path)
    # Text based on page categories. # "Introduction", "Authors", "General Description", "Changes",
    # "Repercussions", "Part Numbers"
    # categories = ["Introduction", "Authors", "General Description", "Changes", "Repercussions", "Part Numbers"]
    categories = ["Part Numbers"]

    for category in categories:
        pdf_text = pdf_doc.get_all_text_data_based_on_page_category(category)
        print(f"category = {category} pdf_text = {pdf_text}")

        # To ensure that the OpenAI client.chat.completions.create method gives consistent answers for the same input
        # data, you need to set the seed parameter in the request.The seed parameter specifies a random seed value
        # that controls the randomization process used by the model.Providing the same seed value for the same input
        # data ensures deterministic behavior, resulting in consistent responses.
        seed_val = string_to_integer_sum_alphabet(os.path.basename(pdf_path))
        # print(f"seed val is {seed_val} for file {os.path.basename(pdf_path)}")

        if USE_GPT_FLAG and 1==2:
            gpt_extract = chat_with_gpt_based_on_category(pdf_text, seed_val, category)
            print(f"For category {category} gpt_extract is = {gpt_extract}")
            gpt_extract_as_arr = gpt_extract.split('\n')

            output = tred_json()
            for each_line in gpt_extract_as_arr:
                in_arr = each_line.split(':')
                if len(in_arr) > 1:
                    key = in_arr[0].strip()
                    val = in_arr[1].strip()
                    split_val = val.split(',')
                    split_val = [s.strip() for s in split_val]

                    if (key == 'Part Numbers in comma separated format' or key == 'VB with suffix and prefix' or
                            key == 'Changes in quantity'):
                        if key == 'Part Numbers in comma separated format':
                            key = 'Affected Part Numbers'
                            # print(f"Part numbers == {split_val}")
                            is_valid_part_numbers = check_part_number(split_val)
                            if is_valid_part_numbers:
                                print(f"All Airbus Part numbers are valid!!!!!!!!!!")
                                output.add_data(key, split_val)
                            else:
                                print(f"Invalid Airbus part numbers in {split_val}")
                        elif key == 'VB with suffix and prefix':
                            key = 'Affected VBs'
                            # print(f"Affected VBs == {split_val}")
                            is_valid_part_numbers = check_part_number(split_val)
                            if is_valid_part_numbers:
                                print(f"All Airbus Part numbers are valid!!!!!!!!!!")
                                output.add_data(key, split_val)
                            else:
                                print(f"Invalid Airbus part numbers in {split_val}")
                        elif key == 'Changes in quantity':
                            key = 'Quantitative Changes'
                            output.add_data(key, split_val)
                    else:
                        output.add_data(key, val)
                elif each_line:
                    print(f"WARNING::Line {each_line} can not be split!")

        #     return output.get_intelligent_output(os.path.basename(pdf_path))
        # else:
        #     return {}

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
