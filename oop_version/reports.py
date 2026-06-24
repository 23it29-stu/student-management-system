from abc import ABC, abstractmethod


class Report(ABC):

    @abstractmethod
    def generate_report(self):
        pass


class PerformanceReport(Report):

    def generate_report(self, students):

        report = []

        for student in students:

            if student.marks >= 90:
                grade = "A"

            elif student.marks >= 75:
                grade = "B"

            elif student.marks >= 60:
                grade = "C"

            else:
                grade = "D"

            report.append(
                f"{student.name} | Marks: {student.marks} | Grade: {grade}"
            )

        return report


class AttendanceReport(Report):

    def generate_report(self, students):

        report = []

        for student in students:

            status = (
                "Eligible"
                if student.attendance >= 75
                else "Defaulter"
            )

            report.append(
                f"{student.name} | Attendance: {student.attendance}% | {status}"
            )

        return report