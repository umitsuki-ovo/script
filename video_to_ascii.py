import cv2
import sys
from PIL import Image
import tqdm

video_path = sys.argv[1]
ascii_image = []

def write_data(ascii_data):
    with open("ascii_data.txt", "a") as f:
        f.write(ascii_data)
        f.write("\n\n")

def image_to_ascii(img):
    # resize the image
    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    # new size of image
    # print(img.size)

    # convert image to greyscale format
    img = img.convert('L')

    pixels = img.getdata()

    # replace each pixel with a character from array
    chars = [".",":","!","*","%","$","@","&","#","S","B"]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    # ascii image
    # print(ascii_image)

    # write to a text file.
    write_data(ascii_image)

def load_video(video_path):
    # open video file
    cap = cv2.VideoCapture(video_path)
    
    # write video fps
    write_data(str(cap.get(cv2.CAP_PROP_FPS)))

    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    for _ in tqdm.tqdm(range(int(float(total_frame)))):
        # load video frame
        ret, frame = cap.read()
    
        # exit
        if not ret:
            break
    
        # cv2 to pil
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)

        image_to_ascii(frame_pil)

    print('\nfin.')
    cap.release()

load_video(video_path)
