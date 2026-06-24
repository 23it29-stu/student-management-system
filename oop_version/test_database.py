from student import Student
from database_manager import DatabaseManager

db = DatabaseManager()

student = Student(
    "999",
    "Test Student",
    "BCA",
    85,
    80
)

db.add_student(student)

print("Student Added Successfully")