import os
import time
import cv2
import numpy as np
from PIL import Image

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getImagesAndLabels(path):
    create_directory(path)
    print(f"Directory checked/created: {path}")
    try:
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return [], []
    print(f"Image paths: {imagePaths}")
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id = getImagesAndLabels("TrainingImage")
    print(f"Number of faces: {len(faces)}, Number of Ids: {len(Id)}")
    try:
        recognizer.train(faces, np.array(Id))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        print("Images trained successfully.")
    except cv2.error as e:
        print(f"Error in training: {e}")
    time.sleep(3)
