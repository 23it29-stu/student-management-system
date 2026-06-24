from student import Student
from reports import (
    PerformanceReport,
    AttendanceReport
)

students = [

    Student(
        "1",
        "Jiya",
        "BCA",
        95,
        85
    ),

    Student(
        "2",
        "Sakshi",
        "B.Tech",
        70,
        60
    )
]

performance = PerformanceReport()

attendance = AttendanceReport()

print("Performance Report")
print("-------------------")

for line in performance.generate_report(students):
    print(line)

print("\nAttendance Report")
print("-------------------")

for line in attendance.generate_report(students):
    print(line)