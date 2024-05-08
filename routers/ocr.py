from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile

from PIL import Image, ImageEnhance
from io import BytesIO
import datetime
import time
import os

from utils.utils import is_image, sizeof_fmt
from utils.utils import transform_image_to_text

# router = APIRouter(
#     prefix="",
#     tags=['OCR']
# )


def single_image_to_json(image_file_path):
    now = datetime.datetime.now()
    start_time = time.time()

    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} [ INFO ] : Processing OCR Scan {image_file_path}")

    #file_handle = open(image_file_path, "r")
    # is_image_check = is_image(file.file)

    # if is_image_check["status"]:
    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} [ INFO ] : Started OCR Scan {image_file_path}")
    image = Image.open(image_file_path)

    # # Enhance brightness
    # brightness_factor = 1.2
    # sharpness_factor = 1.5
    # contrast_factor = 1.2
    # enhancer = ImageEnhance.Brightness(image)
    # image = enhancer.enhance(brightness_factor)
    #
    # # Enhance sharpness
    # enhancer = ImageEnhance.Sharpness(image)
    # image = enhancer.enhance(sharpness_factor)
    #
    # # Enhance contrast
    # enhancer = ImageEnhance.Contrast(image)
    # image = enhancer.enhance(contrast_factor)

    text = transform_image_to_text(image)

    if len(text) == 0:
        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} [ ERROR ] : Finished OCR Scan {image_file_path} : Total duration {str(datetime.timedelta(seconds=time.time() - start_time))}")
        return {"data": text, "msg": "file parsed empty", "status": False, "duration": {str(datetime.timedelta(seconds=time.time() - start_time))}}

    print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} [ INFO ] : Finished OCR Scan {image_file_path} : Total duration {str(datetime.timedelta(seconds=time.time() - start_time))}")
    return {"data": text, "msg": "file parsed successfully", "status": True, "duration": {str(datetime.timedelta(seconds=time.time() - start_time))}}
    # else:
    #     print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} [ ERROR ] : Error OCR Scan {file.filename} : This is not an image")
    #     return {"error": "There is an error in parsing file.", "data": "parsing ERROR", "msg": is_image_check, "status": False}


def single_image_to_text(file: bytes = File()):
    if is_image(BytesIO(file)):
        image = Image.open(BytesIO(file))
        text = transform_image_to_text(image)
        return text
    else:
        return {"error": "This is not an image."}

# def multiple_images_to_json(files: List[UploadFile]):
#     result = list()
#     for file in files:
#
#         fle_result = dict()
#
#         if is_image(file.file):
#
#             image = Image.open(file.file)
#             text = transform_image_to_text(image)
#
#             fle_result["file_name"] = file.filename
#             fle_result["data"] = text
#             fle_result["language"] = language_detection(text)
#
#         else:
#             fle_result["file_name"] = file.filename
#             fle_result["error"] = "This is not an image."
#
#         result.append(fle_result)
#
#     return result
