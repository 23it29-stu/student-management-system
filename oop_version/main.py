import tkinter as tk
from tkinter import messagebox, ttk

from database_manager import DatabaseConnectionError, DatabaseManager
from student import Student


class StudentManagementSystem:
    def __init__(self):
        try:
            self.db = DatabaseManager()
        except DatabaseConnectionError as exc:
            temp_root = tk.Tk()
            temp_root.withdraw()
            messagebox.showerror("Database Error", str(exc))
            temp_root.destroy()
            raise SystemExit(1) from exc

        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f6f9")

        self.create_gui()
        self.load_students()
        self.root.mainloop()

    def create_gui(self):
        title = tk.Label(
            self.root,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 24, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        title.pack(pady=15)

        form_frame = tk.LabelFrame(self.root, text="Student Details", padx=20, pady=20)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(form_frame, width=30)
        self.id_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Name").grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Course").grid(row=2, column=0, padx=10, pady=10)
        self.course_combo = ttk.Combobox(
            form_frame,
            values=["BCA", "MCA", "B.Tech", "M.Tech", "B.Sc", "M.Sc"],
            width=27,
        )
        self.course_combo.grid(row=2, column=1)

        tk.Label(form_frame, text="Marks").grid(row=3, column=0, padx=10, pady=10)
        self.marks_entry = tk.Entry(form_frame, width=30)
        self.marks_entry.grid(row=3, column=1)

        tk.Label(form_frame, text="Attendance (%)").grid(row=4, column=0, padx=10, pady=10)
        self.attendance_entry = tk.Entry(form_frame, width=30)
        self.attendance_entry.grid(row=4, column=1)

        search_frame = tk.Frame(self.root, bg="#f4f6f9")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search Student :", bg="#f4f6f9").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)
        tk.Button(search_frame, text="Search", command=self.search_student_record).pack(side="left")

        button_frame = tk.Frame(self.root, bg="#f4f6f9")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="Add Student", width=15, command=self.add_student).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Update Student", width=15, command=self.update_student).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Delete Student", width=15, command=self.delete_student).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Clear", width=15, command=self.clear_fields).grid(row=0, column=3, padx=10)
        tk.Button(button_frame, text="Student Report", width=18, command=self.show_student_report).grid(row=1, column=0, pady=15)
        tk.Button(button_frame, text="Performance Report", width=18, command=self.show_performance_report).grid(row=1, column=1)
        tk.Button(button_frame, text="Attendance Report", width=18, command=self.show_attendance_report).grid(row=1, column=2)

        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=20)

        scrollbar = ttk.Scrollbar(table_frame)
        columns = ("ID", "Name", "Course", "Marks", "Attendance")

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=self.student_table.yview)
        scrollbar.pack(side="right", fill="y")

        for col in columns:
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=180)

        self.student_table.pack(side="left")
        self.student_table.bind("<<TreeviewSelect>>", self.on_student_select)

    def load_students(self):
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        for student in self.db.get_all_students():
            self.student_table.insert("", tk.END, values=student)

    def get_student_from_form(self):
        return Student(
            self.id_entry.get().strip(),
            self.name_entry.get().strip(),
            self.course_combo.get().strip(),
            self.marks_entry.get().strip(),
            self.attendance_entry.get().strip(),
        )

    def add_student(self):
        try:
            student = self.get_student_from_form()
            self.db.add_student(student)
            messagebox.showinfo("Success", "Student Added Successfully")
            self.load_students()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        try:
            student = self.get_student_from_form()
            self.db.update_student(student)
            messagebox.showinfo("Success", "Student Updated Successfully")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        try:
            student_id = self.id_entry.get()

            if student_id == "":
                messagebox.showerror("Error", "Please select a student")
                return

            if messagebox.askyesno("Delete Student", "Are you sure?"):
                self.db.delete_student(student_id)
                messagebox.showinfo("Success", "Student Deleted Successfully")
                self.load_students()
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.course_combo.set("")
        self.marks_entry.delete(0, tk.END)
        self.attendance_entry.delete(0, tk.END)

    def search_student_record(self):
        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.load_students()
            return

        for row in self.student_table.get_children():
            self.student_table.delete(row)

        for student in self.db.search_student(keyword):
            self.student_table.insert("", tk.END, values=student)

    def on_student_select(self, event):
        selected = self.student_table.focus()

        if not selected:
            return

        values = self.student_table.item(selected, "values")

        self.clear_fields()
        self.id_entry.insert(0, values[0])
        self.name_entry.insert(0, values[1])
        self.course_combo.set(values[2])
        self.marks_entry.insert(0, values[3])
        self.attendance_entry.insert(0, values[4])

    def show_student_report(self):
        selected = self.student_table.focus()

        if not selected:
            messagebox.showerror("Error", "Please select a student")
            return

        values = self.student_table.item(selected, "values")
        student = Student(values[0], values[1], values[2], values[3], values[4])

        report_window = tk.Toplevel(self.root)
        report_window.title("Student Report")
        report_window.geometry("500x350")

        tk.Label(report_window, text="STUDENT REPORT", font=("Arial", 18, "bold")).pack(pady=15)

        report_text = (
            f"Student ID : {student.student_id}\n\n"
            f"Name : {student.name}\n\n"
            f"Course : {student.course}\n\n"
            f"Marks : {student.marks}\n\n"
            f"Grade : {student.calculate_grade()}\n\n"
            f"Attendance : {student.attendance}%\n\n"
            f"Status : {student.attendance_status()}"
        )

        tk.Label(report_window, text=report_text, justify="left", font=("Arial", 12)).pack(padx=20)

    def show_performance_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Performance Report")
        report_window.geometry("750x450")

        tk.Label(report_window, text="STUDENT PERFORMANCE REPORT", font=("Arial", 18, "bold")).pack(pady=15)

        tree = ttk.Treeview(report_window, columns=("Name", "Marks", "Grade"), show="headings")
        tree.heading("Name", text="Student Name")
        tree.heading("Marks", text="Marks")
        tree.heading("Grade", text="Grade")
        tree.column("Name", width=300)
        tree.column("Marks", width=150)
        tree.column("Grade", width=150)
        tree.pack(fill="both", expand=True, padx=20, pady=20)

        for row in self.db.get_all_students():
            student = Student(row[0], row[1], row[2], row[3], row[4])
            tree.insert("", tk.END, values=(student.name, student.marks, student.calculate_grade()))

    def show_attendance_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Attendance Report")
        report_window.geometry("750x450")

        tk.Label(report_window, text="STUDENT ATTENDANCE REPORT", font=("Arial", 18, "bold")).pack(pady=15)

        tree = ttk.Treeview(report_window, columns=("Name", "Attendance", "Status"), show="headings")
        tree.heading("Name", text="Student Name")
        tree.heading("Attendance", text="Attendance (%)")
        tree.heading("Status", text="Status")
        tree.column("Name", width=300)
        tree.column("Attendance", width=150)
        tree.column("Status", width=150)
        tree.pack(fill="both", expand=True, padx=20, pady=20)

        for row in self.db.get_all_students():
            student = Student(row[0], row[1], row[2], row[3], row[4])
            tree.insert("", tk.END, values=(student.name, f"{student.attendance}%", student.attendance_status()))


if __name__ == "__main__":
    StudentManagementSystem()