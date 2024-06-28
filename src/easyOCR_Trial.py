import tempfile

# import torch
# print(torch.__version__)
# print(torch.cuda.is_available())
# print(torch.backends.cudnn.enabled)

import easyocr
import cv2
import matplotlib.pyplot as plt

temp_directory = tempfile.gettempdir()
print(f"temp_directory = {temp_directory}")
image_path = f"{temp_directory}/page7_image3.jpg"

# Load the image using OpenCV
# image_path = 'path/to/your/image.png'  # Update this path as needed
image = cv2.imread(image_path)

# Convert the image to RGB (EasyOCR requires RGB format)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the languages you need

# Perform OCR
results = reader.readtext(image_rgb)

# Print the results
for (bbox, text, prob) in results:
    print(f'Text: {text}, Probability: {prob:.4f}')

    # Draw bounding boxes around detected text
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    cv2.rectangle(image_rgb, top_left, bottom_right, (0, 255, 0), 2)

# Display the image with bounding boxes
plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.show()
