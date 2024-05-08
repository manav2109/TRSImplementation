import langdetect
import pytesseract
import base64
from PIL import Image, TiffImagePlugin

Image.MAX_IMAGE_PIXELS = 1000000000


def language_detection(text, method="single"):
    """
    @desc:
    - detects the language of a text
    @params:
    - text: the text which language needs to be detected
    - method: detection method:
        single: if the detection is based on the first option (detect)
    @return:
    - the langue/list of languages
    """

    try:
        if method.lower() != "single":
            result = langdetect.detect_langs(text)
        else:
            result = langdetect.detect(text)
        return result

    except langdetect.lang_detect_exception.LangDetectException:
        return ""


def is_image(file):
    try:
        img = Image.open(file)
        return {"status": True, "message": None}
    except Exception as e:
        print("Open file error")
        print(e)
        print("Open file error")
        return {"status": False, "message": f"{e}"}


def transform_image_to_text(image):
    page = 0
    text = ""
    while True:
        try:
            image.seek(page)
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n\n"
            page += 1
        except Exception as e:
            print(f"{e}")
            break

    return text


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False
