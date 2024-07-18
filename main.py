import os
import sqlite3
import check_camera
import Capture_Image
import Train_Image
import Recognize
import utils
import datetime
import getpass
from automail import send_automail

DATABASE = "school_management.db"

def setup_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'sub_admin', 'teacher'))
        );

        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        );
    ''')
    conn.commit()

    # Ensure the role column has the correct constraint
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'role' in columns:
        cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")
        create_table_sql = cursor.fetchone()[0]
        if "CHECK (role IN ('admin', 'sub_admin', 'teacher'))" not in create_table_sql:
            cursor.execute("ALTER TABLE users RENAME TO users_old")
            cursor.executescript('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'sub_admin', 'teacher'))
                );
                INSERT INTO users (id, username, password, role) SELECT id, username, password, role FROM users_old;
                DROP TABLE users_old;
            ''')
            conn.commit()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admin_exists = cursor.fetchone()[0]
    if not admin_exists:
        create_admin_account(cursor)
    conn.commit()
    conn.close()

def create_admin_account(cursor):
    print("No admin account found. Please create an admin account.")
    while True:
        username = input("Enter admin username: ")
        password = getpass.getpass("Enter admin password: ")
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')", (username, password))
            print(f"Admin account '{username}' created successfully.")
            break
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose another username.")

def title_bar():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\t**********************************************")
    print("\t***** Face Recognition Attendance System *****")
    print("\t********** By FINIXIA DEDECONS ************")

def welcome():
    title_bar()
    print("Welcome to the School Management System")
    print("Author: Finixia Dedecons")
    user_login()

def user_login():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Login successful")
        role = user[3]
        mainMenu(role)
    else:
        print("Invalid credentials")
        user_login()

def mainMenu(role):
    title_bar()
    if role == 'admin':
        print(10 * "*", "ADMIN MENU", 10 * "*")
        print("[1] Check Camera")
        print("[2] Capture Faces")
        print("[3] Train Images")
        print("[4] Recognize & Attendance")
        print("[5] Auto Mail")
        print("[6] Clear Student Data")
        print("[7] Clear Attendance Logs by Date")
        print("[8] Create Teacher Account")
        print("[9] View Teacher Data")
        print("[10] View Student Data")
        print("[11] Create Sub-Admin Account")
        print("[12] List All Users (Debug)")
        print("[13] Clear All Users (Debug)")
        print("[14] Delete Student by Name")
        print("[15] Delete User by Name")
        print("[16] Delete Teacher by Name")
        print("[17] Quit")
    elif role == 'sub_admin':
        print(10 * "*", "SUB-ADMIN MENU", 10 * "*")
        print("[1] View Teacher Data")
        print("[2] View Student Data")
        print("[3] Create Teacher Account")
        print("[4] Create Student Account")
        print("[5] Delete Student by Name")
        print("[6] Delete Teacher by Name")
        print("[7] Auto Mail")
        print("[8] Quit")
    elif role == 'teacher':
        print(10 * "*", "TEACHER MENU", 10 * "*")
        print("[1] Check Camera")
        print("[2] Capture Faces")
        print("[3] Train Images")
        print("[4] Recognize & Attendance")
        print("[5] Auto Mail")
        print("[6] View Student Data")
        print("[7] Delete Student by Name")
        print("[8] Quit")
    
    while True:
        try:
            choice = int(input("Enter Choice: "))
            if role == 'admin':
                if choice == 1:
                    checkCamera(role)
                elif choice == 2:
                    CaptureFaces(role)
                elif choice == 3:
                    Trainimages(role)
                elif choice == 4:
                    RecognizeFaces(role)
                elif choice == 5:
                    send_automail(role)
                elif choice == 6:
                    clearStudentData(role)
                elif choice == 7:
                    clearAttendanceByDate(role)
                elif choice == 8:
                    create_teacher_account(role)
                elif choice == 9:
                    view_teacher_data(role)
                elif choice == 10:
                    view_student_data(role)
                elif choice == 11:
                    create_sub_admin_account(role)
                elif choice == 12:
                    list_all_users(role)
                elif choice == 13:
                    clear_all_users(role)
                elif choice == 14:
                    delete_student_by_name(role)
                elif choice == 15:
                    delete_user_by_name(role)
                elif choice == 16:
                    delete_teacher_by_name(role)
                elif choice == 17:
                    print("Thank You")
                    break
                else:
                    print("Invalid Choice. Enter 1-17")
            elif role == 'sub_admin':
                if choice == 1:
                    view_teacher_data(role)
                elif choice == 2:
                    view_student_data(role)
                elif choice == 3:
                    create_teacher_account(role)
                elif choice == 4:
                    create_student_account(role)
                elif choice == 5:
                    delete_student_by_name(role)
                elif choice == 6:
                    delete_teacher_by_name(role)
                elif choice == 7:
                    send_automail(role)
                elif choice == 8:
                    print("Thank You")
                    break
                else:
                    print("Invalid Choice. Enter 1-8")
            elif role == 'teacher':
                if choice == 1:
                    checkCamera(role)
                elif choice == 2:
                    CaptureFaces(role)
                elif choice == 3:
                    Trainimages(role)
                elif choice == 4:
                    RecognizeFaces(role)
                elif choice == 5:
                    send_automail(role)
                elif choice == 6:
                    view_student_data(role)
                elif choice == 7:
                    delete_student_by_name(role)
                elif choice == 8:
                    print("Thank You")
                    break
                else:
                    print("Invalid Choice. Enter a valid option\n Try Again")
        except ValueError:
            print("Invalid Choice. Enter a valid option\n Try Again")
    input("Press Enter to exit...")

def checkCamera(role):
    check_camera.camer()
    input("Enter any key to return to main menu")
    mainMenu(role)

def CaptureFaces(role):
    Capture_Image.takeImages()
    input("Enter any key to return to main menu")
    mainMenu(role)

def Trainimages(role):
    Train_Image.TrainImages()
    input("Enter any key to return to main menu")
    mainMenu(role)

def RecognizeFaces(role):
    Recognize.recognize_attendance()
    input("Enter any key to return to main menu")
    mainMenu(role)

def clearStudentData(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    conn.commit()
    conn.close()
    print("All student data cleared.")
    input("Enter any key to return to main menu")
    mainMenu(role)

def clearAttendanceByDate(role):
    date_str = input("Enter the date (YYYY-MM-DD) for which to clear attendance logs: ")
    print(f"Attendance logs for {date_str} cleared.")
    input("Enter any key to return to main menu")
    mainMenu(role)

def create_teacher_account(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    username = input("Enter teacher username: ")
    password = getpass.getpass("Enter teacher password: ")
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'teacher')", (username, password))
        conn.commit()
        print(f"Teacher account '{username}' created successfully.")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("Username already exists. Please choose another username.")
        elif "CHECK constraint failed" in str(e):
            print("Role constraint failed. Please check the role value.")
    conn.close()
    input("Enter any key to return to main menu")
    mainMenu(role)

def create_student_account(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    try:
        cursor.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
        conn.commit()
        print(f"Student account for '{name}' created successfully.")
    except sqlite3.IntegrityError:
        print("Student ID already exists. Please choose another ID.")
    conn.close()
    input("Enter any key to return to main menu")
    mainMenu(role)

def create_sub_admin_account(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    username = input("Enter sub-admin username: ")
    password = getpass.getpass("Enter sub-admin password: ")
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'sub_admin')", (username, password))
        conn.commit()
        print(f"Sub-admin account '{username}' created successfully.")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("Username already exists. Please choose another username.")
        elif "CHECK constraint failed" in str(e):
            print("Role constraint failed. Please check the role value.")
    conn.close()
    input("Enter any key to return to main menu")
    mainMenu(role)

def view_teacher_data(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE role = 'teacher'")
    teachers = cursor.fetchall()
    conn.close()
    if teachers:
        print("Teacher Data:")
        for teacher in teachers:
            print(f"Username: {teacher[0]}")
    else:
        print("Don't have any data of teachers, please add data.")
    input("Enter any key to return to main menu")
    mainMenu(role)

def view_student_data(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    if students:
        print("Student Data:")
        for student in students:
            print(f"Student ID: {student[1]}, Name: {student[2]}")
    else:
        print("Don't have any data of students, please add data.")
    input("Enter any key to return to main menu")
    mainMenu(role)

def delete_student_by_name(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    name = input("Enter the name of the student to delete: ")
    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    student = cursor.fetchone()
    if student:
        cursor.execute("DELETE FROM students WHERE name = ?", (name,))
        conn.commit()
        print(f"Student '{name}' deleted successfully.")
    else:
        print(f"Student '{name}' not found or already deleted.")
    conn.close()
    input("Enter any key to return to main menu")
    mainMenu(role)

def delete_teacher_by_name(role):
    if role in ['admin', 'sub_admin']:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        username = input("Enter the username of the teacher to delete: ")
        cursor.execute("SELECT * FROM users WHERE username = ? AND role = 'teacher'", (username,))
        teacher = cursor.fetchone()
        if teacher:
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            print(f"Teacher '{username}' deleted successfully.")
        else:
            print(f"Teacher '{username}' not found or already deleted.")
        conn.close()
        input("Enter any key to return to main menu")
        mainMenu(role)
    else:
        print("You do not have permission to delete teachers.")
        mainMenu(role)

def delete_user_by_name(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    username = input("Enter the username of the user to delete: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found or already deleted.")
    conn.close()
    input("Enter any key to return to main menu")
    mainMenu(role)

def list_all_users(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    if users:
        print("All Users:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")
    else:
        print("No user data found.")
    input("Enter any key to return to main menu")
    mainMenu(role)

def clear_all_users(role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("All user data cleared.")
    input("Enter any key to return to main menu")
    mainMenu(role)

if __name__ == "__main__":
    setup_database()
    try:
        welcome()
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to exit...")

