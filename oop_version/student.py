class Student:

    def __init__(
        self,
        student_id,
        name,
        course,
        marks,
        attendance
    ):

        self.student_id = student_id
        self.name = name
        self.course = course
        self.marks = float(marks)
        self.attendance = float(attendance)

    def calculate_grade(self):

        if self.marks >= 90:
            return "A"

        elif self.marks >= 75:
            return "B"

        elif self.marks >= 60:
            return "C"

        else:
            return "D"

    def attendance_status(self):

        if self.attendance >= 75:
            return "Eligible"

        return "Defaulter"

    def to_tuple(self):

        return (
            self.student_id,
            self.name,
            self.course,
            self.marks,
            self.attendance
        )