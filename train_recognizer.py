import cv2
import os
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def train_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(resource_path('haarcascade_frontalface_default.xml'))

    faces, ids = [], []

    def get_images_and_labels(path):
        for image_name in os.listdir(path):
            if image_name.endswith('.jpg'):
                image_path = os.path.join(path, image_name)
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                id = int(image_name.split('.')[1])
                faces.append(gray)
                ids.append(id)

    get_images_and_labels('TrainingImage')

    recognizer.train(faces, np.array(ids))
    recognizer.save('TrainingImageLabel/Trainner.yml')

train_face_recognizer()
