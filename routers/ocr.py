from PIL import Image
from utils.utils import transform_image_to_text


def single_image_to_json(image, image_file_path):
    image = Image.open(image_file_path)
    text = transform_image_to_text(image)
    return [line.strip() for line in text.split('\n') if line.strip()]

