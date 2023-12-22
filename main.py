# Install Package pip install opencv-python
# Or goto python package search opencv-python and install it
import time

import cv2

video = cv2.VideoCapture(0)

time.sleep(1)

while True:
    check, frame = video.read()
    cv2.imshow("my video",frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

