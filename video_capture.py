import cv2

def capture(video_path, frame_num, time):
    cap = cv2.VideoCapture(video_path)
    if time=='-s':
        frame_num = int(cap.get(cv2.CAP_PROP_FPS) * frame_num)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f'capture_{frame_num}.jpg', frame)
        print(f'Frame captured and saved as capture_{frame_num}.jpg')
    else:
        print("Error: Failed to capture frame.")
    cap.release()

video_path = sys.argv[1]
frame_num = int(sys.argv[2])
time = sys.argv[3]
capture(video_path, frame_num, time)
