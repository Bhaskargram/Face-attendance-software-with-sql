import datetime
import os
import time
import cv2
import pandas as pd

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    return recognizer

def load_cascade():
    harcascadePath = "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(harcascadePath)

def get_attendance_file():
    today = datetime.datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    day_name = today.strftime("%A")
    attendance_file = f"Attendance/Attendance_{date_str}_{day_name}.csv"
    return attendance_file

def ensure_attendance_file_exists(file_path):
    col_names = ['Id', 'Name', 'Date', 'Time']
    if not os.path.exists(file_path):
        attendance = pd.DataFrame(columns=col_names)
        attendance.to_csv(file_path, index=False)

def recognize_attendance():
    recognizer = load_recognizer()
    faceCascade = load_cascade()
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX

    ensure_directory_exists("Attendance")
    attendance_file = get_attendance_file()
    ensure_attendance_file_exists(attendance_file)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    recognized_faces = set()

    while True:
        ret, im = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, 
            minSize=(int(minW), int(minH)), flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 100:
                name = df.loc[df['Id'] == Id]['Name'].values[0] if not df[df['Id'] == Id].empty else 'Unknown'
                confstr = "  {0}%".format(round(100 - conf))
                tt = f"{Id}-{name}"

                if (100 - conf) > 67 and Id not in recognized_faces:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    attendance_data = pd.DataFrame([[Id, name, date, timeStamp]], columns=['Id', 'Name', 'Date', 'Time'])
                    attendance_data.to_csv(attendance_file, mode='a', header=False, index=False)
                    print(f"Attendance logged: ID {Id}, Name {name}, Date {date}, Time {timeStamp}")
                    recognized_faces.add(Id)
                    cam.release()
                    cv2.destroyAllWindows()
                    return

                if (100 - conf) > 67:
                    tt += " [Pass]"
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                conf_color = (0, 255, 0) if (100 - conf) > 67 else (0, 255, 255) if (100 - conf) > 50 else (0, 0, 255)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, conf_color, 1)

        cv2.imshow('Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def clear_attendance():
    attendance_dir = "Attendance"
    for file in os.listdir(attendance_dir):
        file_path = os.path.join(attendance_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("All attendance logs cleared.")

def clear_attendance_by_date(date_str):
    attendance_dir = "Attendance"
    for file in os.listdir(attendance_dir):
        if date_str in file:
            file_path = os.path.join(attendance_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Attendance log for {date_str} cleared.")
    print(f"No attendance log found for {date_str}.")

if __name__ == "__main__":
    while True:
        choice = input("Enter 'r' to recognize attendance, 'c' to clear all attendance logs, or 'd' to clear attendance logs by date: ").lower()
        if choice == 'r':
            recognize_attendance()
        elif choice == 'c':
            clear_attendance()
        elif choice == 'd':
            date_str = input("Enter the date (YYYY-MM-DD) for which to clear attendance logs: ")
            clear_attendance_by_date(date_str)
        else:
            print("Invalid choice. Please enter 'r', 'c', or 'd'.")
