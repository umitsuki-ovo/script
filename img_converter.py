import os
import sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def convert_image(img_path, ext):
    image = Image.open(img_path)
    file_path = os.path.splitext(os.path.basename(img_path))[0] + '.' + ext
    image = image.convert('RGB')
    image.save(file_path, format=ext.upper())
    print(f"Image saved as {file_path}")

img_path = sys.argv[1]
ext = sys.argv[2]
convert_image(img_path, ext)
