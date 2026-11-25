
import json
from langchain.tools import tool

# Load course data
with open("data/courses.json", "r") as file:
    courses = json.load(file)

# Load student data
with open("data/students.json", "r") as file:
    students = json.load(file)


@tool
def check_prerequisites(student_id: str, course_code: str) -> str:
    """
    Check whether a student is eligible to take a course.
    Requires student ID and course code.
    """

    student = students.get(student_id)
    course = courses.get(course_code)

    if not student:
        return "Student not found."

    if not course:
        return "Course not found."

    completed = student["completed_courses"]
    required = course["prerequisites"]

    missing = [
        c for c in required if c not in completed
    ]

    if missing:
        return f"Not eligible. Missing: {missing}"

    return "Eligible! You can take this course."
