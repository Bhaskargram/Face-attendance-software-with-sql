# check_camera.py

import os
import sys
import cv2
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

cascPath = resource_path('haarcascade_frontalface_default.xml')

def camer():
    face_cascade = cv2.CascadeClassifier(cascPath)

    if face_cascade.empty():
        raise Exception(f"Failed to load cascade classifier from {cascPath}")

    cap = cv2.VideoCapture(0)
    face_detected = False
    start_time = None

    while True:
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
            if not face_detected:
                face_detected = True
                start_time = time.time()

        cv2.imshow('Webcam Check', img)

        if face_detected and (time.time() - start_time) > 5:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
