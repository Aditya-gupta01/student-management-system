# In main file
# import script1
# print(script1.sum(1, 3))

import sqlite3


# =========================
# DATABASE CONNECTION
# =========================

connection = sqlite3.connect("students.db")
cursor = connection.cursor()


# =========================
# CREATE TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    course TEXT NOT NULL,
    email TEXT,
    marks REAL
)
""")

connection.commit()


# =========================
# ADD STUDENT
# =========================

def add_student():

    print("\n===== ADD STUDENT =====")

    name = input("Enter name: ").strip()
    roll_no = input("Enter roll number: ").strip()
    course = input("Enter course: ").strip()
    email = input("Enter email: ").strip()

    try:
        marks = float(input("Enter marks: "))
    except ValueError:
        print("Invalid marks. Please enter a number.")
        return

    if not name or not roll_no or not course:
        print("Name, roll number and course are required.")
        return

    try:
        cursor.execute("""
        INSERT INTO students (name, roll_no, course, email, marks)
        VALUES (?, ?, ?, ?, ?)
        """, (name, roll_no, course, email, marks))

        connection.commit()

        print("\nStudent added successfully!")

    except sqlite3.IntegrityError:
        print("\nRoll number already exists.")


# =========================
# VIEW STUDENTS
# =========================

def view_students():

    print("\n===== ALL STUDENTS =====")

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
        return

    for student in students:

        print("\nID:", student[0])
        print("Name:", student[1])
        print("Roll No:", student[2])
        print("Course:", student[3])
        print("Email:", student[4])
        print("Marks:", student[5])
        print("------------------------")


# =========================
# SEARCH STUDENT
# =========================

def search_student():

    print("\n===== SEARCH STUDENT =====")

    roll_no = input("Enter roll number: ").strip()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:

        print("\nStudent Found!")
        print("ID:", student[0])
        print("Name:", student[1])
        print("Roll No:", student[2])
        print("Course:", student[3])
        print("Email:", student[4])
        print("Marks:", student[5])

    else:
        print("\nStudent not found.")


# =========================
# UPDATE STUDENT
# =========================

def update_student():

    print("\n===== UPDATE STUDENT =====")

    roll_no = input("Enter roll number: ").strip()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if not student:
        print("\nStudent not found.")
        return

    print("\nEnter new details.")

    name = input("New name: ").strip()
    course = input("New course: ").strip()
    email = input("New email: ").strip()

    try:
        marks = float(input("New marks: "))
    except ValueError:
        print("Invalid marks.")
        return

    cursor.execute("""
    UPDATE students
    SET name = ?, course = ?, email = ?, marks = ?
    WHERE roll_no = ?
    """, (name, course, email, marks, roll_no))

    connection.commit()

    print("\nStudent updated successfully!")


# =========================
# DELETE STUDENT
# =========================

def delete_student():

    print("\n===== DELETE STUDENT =====")

    roll_no = input("Enter roll number: ").strip()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if not student:
        print("\nStudent not found.")
        return

    confirm = input(
        "Are you sure you want to delete this student? (yes/no): "
    ).lower()

    if confirm == "yes":

        cursor.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll_no,)
        )

        connection.commit()

        print("\nStudent deleted successfully!")

    else:
        print("\nDelete cancelled.")


# =========================
# MAIN MENU
# =========================

def main():

    while True:

        print("\n")
        print("================================")
        print("     STUDENT MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("\nThank you for using Student Management System.")
            break

        else:
            print("\nInvalid choice. Please try again.")


# =========================
# PROGRAM START
# =========================

try:
    main()

finally:
    connection.close()