import os
import sys
import cv2
import time

# Function to get the correct path to the XML file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Use the function to get the path to the haarcascade file
cascPath = resource_path('haarcascade_frontalface_default.xml')

def camer():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cascPath)

    if face_cascade.empty():
        raise Exception(f"Failed to load cascade classifier from {cascPath}")

    # To capture video from webcam.
    cap = cv2.VideoCapture(0)

    face_detected = False
    start_time = None

    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
            if not face_detected:
                face_detected = True
                start_time = time.time()

        # Display
        cv2.imshow('Webcam Check', img)

        # Stop if face detected for 5 seconds
        if face_detected and (time.time() - start_time) > 5:
            break

        # Stop if escape key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
