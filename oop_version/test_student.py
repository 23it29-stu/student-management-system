from student import Student

student = Student(
    "101",
    "Jiya",
    "BCA",
    85,
    80
)

print("Name:", student.name)
print("Grade:", student.calculate_grade())
print("Attendance:", student.attendance_status())