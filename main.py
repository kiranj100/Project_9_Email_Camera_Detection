# Install Package pip install opencv-python
# Or goto python package search opencv-python and install it
import glob
import os
import time
import cv2
from emailing import send_mail
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)



while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # First frame is none when it hold first frame is regular frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # see the difference
    # when frame is stable it also none and when camera capture
    # some moment then its compare first frame and gray frame gua
    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    # if frame is more than 60 then it's equal to 255 it white color pixel
    # it is list, so we want to second item in that list and list start with
    # zero so 1 is on second position
    thresh_frame = cv2.threshold(delta_frame,60,255, cv2.THRESH_BINARY)[1]
    # dilate frame is reduce the noice of frame and iteration number higher
    # It also means that the video noice is reduced
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow("my video", dil_frame)

    cont, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for counter in cont:
        # its for not detecting fake object
        if cv2.contourArea(counter) < 5000:
            continue
        # its creating a frame if any object is moving and capture it specific
        # Frame structure with height and width
        x, y, w, h = cv2.boundingRect(counter)

        # It draws in color frame rectangle for detecting that object
        # x and y is plus height and width and bgr color
        # 255 is High value in that tuple so its means its green color
        rectangle = cv2.rectangle(frame, (x, y),(x+w, y+h), (0,255, 0), 3)

        # .any() or all() capture the many frames to resolve ambiguity problem
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    # we want status value 1 so zero to 1 only
    status_list = status_list[-2:]

    # first time the status is zero and when status change that value one
    # that means some object is detected and when object is passed and its
    # convert into zero then capture it and send us Email
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_mail, args=(image_with_object, ))
        email_thread.daemon = True

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()


    print(status_list)

    cv2.imshow("Video",frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break
video.release()
clean_thread.start()
