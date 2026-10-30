import json
import os
from datetime import datetime

FILE_NAME = "students.json"


# Load student data from file
def load_students():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read student data.")
    return []


# Save student data to file
def save_students(students):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        print("Error: Unable to save student data.")
        return False


# Generate a new student ID
def generate_id(students):
    if not students:
        return 1
    return max(student["id"] for student in students) + 1


# Add a new student
def add_student(students):
    print("\n--- Add New Student ---")

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Enter student age: "))
        if age < 1 or age > 120:
            print("Enter a valid age.")
            return
    except ValueError:
        print("Age must be a number.")
        return

    course = input("Enter course name: ").strip()
    email = input("Enter email address: ").strip()

    if not course:
        print("Course cannot be empty.")
        return

    student = {
        "id": generate_id(students),
        "name": name,
        "age": age,
        "course": course,
        "email": email,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.append(student)

    if save_students(students):
        print("Student added successfully!")
        print("Student ID:", student["id"])
    else:
        students.pop()


# Display one student
def display_student(student):
    print("-" * 40)
    print("Student ID :", student["id"])
    print("Name       :", student["name"])
    print("Age        :", student["age"])
    print("Course     :", student["course"])
    print("Email      :", student["email"])
    print("Created At :", student["created_at"])


# View all students
def view_students(students):
    print("\n--- All Students ---")

    if not students:
        print("No students found.")
        return

    for student in students:
        display_student(student)

    print("-" * 40)
    print("Total students:", len(students))


# Search student by ID
def search_student(students):
    print("\n--- Search Student ---")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for student in students:
        if student["id"] == student_id:
            display_student(student)
            return

    print("Student not found.")


# Search student by name
def search_by_name(students):
    name = input("Enter student name to search: ").strip().lower()

    if not name:
        print("Please enter a name.")
        return

    found = [
        student for student in students
        if name in student["name"].lower()
    ]

    if found:
        for student in found:
            display_student(student)
    else:
        print("No matching student found.")


# Update student details
def update_student(students):
    print("\n--- Update Student ---")

    try:
        student_id = int(input("Enter student ID to update: "))
    except ValueError:
        print("Invalid student ID.")
        return

    for student in students:
        if student["id"] == student_id:
            display_student(student)

            print("\nLeave a field blank to keep its current value.")

            name = input("New name: ").strip()
            age = input("New age: ").strip()
            course = input("New course: ").strip()
            email = input("New email: ").strip()

            if name:
                student["name"] = name

            if age:
                try:
                    new_age = int(age)
                    if new_age < 1 or new_age > 120:
                        print("Invalid age. Age was not changed.")
                    else:
                        student["age"] = new_age
                except ValueError:
                    print("Invalid age. Age was not changed.")

            if course:
                student["course"] = course

            if email:
                student["email"] = email

            if save_students(students):
                print("Student updated successfully!")
            return

    print("Student not found.")


# Delete a student
def delete_student(students):
    print("\n--- Delete Student ---")

    try:
        student_id = int(input("Enter student ID to delete: "))
    except ValueError:
        print("Invalid student ID.")
        return

    for index, student in enumerate(students):
        if student["id"] == student_id:
            display_student(student)

            confirm = input(
                "Are you sure you want to delete? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                removed = students.pop(index)

                if save_students(students):
                    print("Student deleted successfully!")
                else:
                    students.insert(index, removed)
            else:
                print("Delete cancelled.")
            return

    print("Student not found.")


# Sort students by name
def sort_students(students):
    print("\n--- Sort Students ---")
    print("1. Sort by name A-Z")
    print("2. Sort by age")
    print("3. Sort by student ID")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        sorted_students = sorted(
            students, key=lambda student: student["name"].lower()
        )
    elif choice == "2":
        sorted_students = sorted(
            students, key=lambda student: student["age"]
        )
    elif choice == "3":
        sorted_students = sorted(
            students, key=lambda student: student["id"]
        )
    else:
        print("Invalid choice.")
        return

    if not sorted_students:
        print("No students to sort.")
        return

    for student in sorted_students:
        display_student(student)


# Display statistics
def show_statistics(students):
    print("\n--- Student Statistics ---")

    if not students:
        print("No student data available.")
        return

    total = len(students)
    average_age = sum(s["age"] for s in students) / total

    course_counts = {}

    for student in students:
        course = student["course"]
        course_counts[course] = course_counts.get(course, 0) + 1

    print("Total students:", total)
    print("Average age:", round(average_age, 2))

    print("\nStudents by course:")

    for course, count in sorted(course_counts.items()):
        print(f"{course}: {count}")


# Main menu
def main():
    students = load_students()

    while True:
        print("\n" + "=" * 45)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Search Student by Name")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Sort Students")
        print("8. Show Statistics")
        print("9. Exit")
        print("=" * 45)

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            view_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            search_by_name(students)

        elif choice == "5":
            update_student(students)

        elif choice == "6":
            delete_student(students)

        elif choice == "7":
            sort_students(students)

        elif choice == "8":
            show_statistics(students)

        elif choice == "9":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please select 1 to 9.")


if __name__ == "__main__":
    main()
