import os
import sys
import time

ascii_path = sys.argv[1]
adjust = 1.14 # Modify this variable to fit your environment as necessary.

def load_ascii(ascii_path):
    with open(ascii_path, 'r') as file:
        ascii_data = file.read()
        data = ascii_data.split('\n\n')
    return data

def play_animation(data, fps):
    os.system('cls')
    delay = 1.0 / (fps * adjust)
    for ascii in data:
        print("\033[H", end="")
        print(ascii)
        time.sleep(delay)

def main():
    print('loading...')
    data = load_ascii(ascii_path)
    fps = int(float(data.pop(0)))
    play_animation(data, fps)

main()
