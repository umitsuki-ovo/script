from PIL import Image
from tqdm import tqdm
import os

def split(image_path, size):
    image = Image.open(image_path)
    dpi = image.info.get('dpi', (72, 72))
    dpi_x, dpi_y = dpi

    paper_sizes = {
        "A5": (148, 210),
        "A4": (210, 297),
        "B4": (257, 364),
        "B5": (182, 257),
    }

    paper_pixels = {key: (int(width / 25.4 * dpi_x), int(height / 25.4 * dpi_y)) for key, (width, height) in paper_sizes.items()}
    width, height = image.size
    paper_width, paper_height = paper_pixels[size]
    splits_width = width // paper_width
    splits_height = height // paper_height

    splits = []
    total_splits = splits_height * splits_width
    progress_bar = tqdm(total=total_splits, desc="Processing Splits", unit="split")

    for i in range(splits_height):
        for j in range(splits_width):
            left = j * paper_width
            upper = i * paper_height
            right = left + paper_width
            lower = upper + paper_height

            split_image = image.crop((left, upper, right, lower))
            splits.append(split_image)
            split_image.save(f'{size}_{os.path.splitext(os.path.basename(image_path))[0]}_{i}_{j}{os.path.splitext(image_path)[1].lower()}')
            progress_bar.update(1)
    print(f"The image has been divided into {splits_height} rows and {splits_width} columns and {total_splits} photos.")

image_path = input()
size = input()

split(image_path, size)
