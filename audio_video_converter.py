import ffmpeg
import sys
import os

video_ext = ['mp4', 'avi', 'mov', 'mkv']
audio_ext = ['mp3', 'aac', 'wav', 'flac']

def convert_video(file, ext):
    output_file = os.path.splitext(file)[0] + '.' + ext
    try:
        ffmpeg.input(file).output(output_file, vcodec='libx264', acodec='aac').run()
        print(f"converted")
    except ffmpeg.Error as e:
        print("Error:", e.stderr if e.stderr else str(e))

def extract_video_to_audio(file, ext):
    output_file = os.path.splitext(file)[0] + '.' + ext
    try:
        ffmpeg.input(file).output(output_file, vn=None, acodec='libmp3lame').run()
        print(f"converted")
    except ffmpeg.Error as e:
        print("Error:", e.stderr if e.stderr else str(e))

def convert_audio(file, ext):
    output_file = os.path.splitext(file)[0] + '.' + ext
    try:
        ffmpeg.input(file).output(output_file, acodec='libmp3lame').run()
        print(f"converted")
    except ffmpeg.Error as e:
        print("Error:", e.stderr if e.stderr else str(e))

def auto_convert(file_path, ext):
    file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
    if file_ext in video_ext:
        if ext in audio_ext:
            extract_video_to_audio(file_path, ext)
        else:
            convert_video(file_path, ext)
    elif file_ext in audio_ext:
        convert_audio(file_path, ext)
    else:
        print(f"{ext} is not supported.")

file_path = sys.argv[1]
ext = sys.argv[2]

auto_convert(file_path, ext)
