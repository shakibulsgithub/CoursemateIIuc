from tools import check_prerequisites

result = check_prerequisites.invoke({
    "student_id": "S-014",
    "course_code": "CSE-2101"
})

print(result)