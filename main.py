import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    add_student,
    get_all_students,
    update_student,
    delete_student,
    search_student,
    get_performance_report
)


# ---------------- FUNCTIONS ---------------- #

def save_student():

    try:
        student_id = id_entry.get().strip()
        name = name_entry.get().strip()
        course = course_combo.get().strip()
        marks = marks_entry.get().strip()
        attendance = attendance_entry.get().strip()

        if not student_id or not name or not course or not marks or not attendance:
            messagebox.showerror("Error", "All fields are required!")
            return

        add_student(
            student_id,
            name,
            course,
            float(marks),
            float(attendance)
        )

        messagebox.showinfo(
            "Success",
            "Student Added Successfully!"
        )

        clear_fields()
        load_students()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_combo.set("")
    marks_entry.delete(0, tk.END)
    attendance_entry.delete(0, tk.END)


def load_students():

    for row in tree.get_children():
        tree.delete(row)

    students = get_all_students()

    for student in students:
        tree.insert("", tk.END, values=student)
    
def select_student(event):

    selected = tree.focus()

    values = tree.item(selected, "values")

    if values:

        id_entry.delete(0, tk.END)
        id_entry.insert(0, values[0])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        course_combo.set(values[2])

        marks_entry.delete(0, tk.END)
        marks_entry.insert(0, values[3])

        attendance_entry.delete(0, tk.END)
        attendance_entry.insert(0, values[4])

def update_selected_student():

    try:

        student_id = id_entry.get()
        name = name_entry.get()
        course = course_combo.get()
        marks = float(marks_entry.get())
        attendance = float(attendance_entry.get())

        update_student(
            student_id,
            name,
            course,
            marks,
            attendance
        )

        messagebox.showinfo(
            "Success",
            "Student Updated Successfully!"
        )

        load_students()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def delete_selected_student():

    try:

        student_id = id_entry.get()

        if not student_id:
            messagebox.showerror(
                "Error",
                "Please select a student"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if confirm:

            delete_student(student_id)

            messagebox.showinfo(
                "Success",
                "Student Deleted Successfully!"
            )

            clear_fields()
            load_students()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def search_student_record():

    keyword = search_entry.get().strip()

    if keyword == "":
        load_students()
        return

    students = search_student(keyword)

    for row in tree.get_children():
        tree.delete(row)

    for student in students:
        tree.insert("", tk.END, values=student)

def performance_report():

    report_window = tk.Toplevel(root)
    report_window.title("Performance Report")
    report_window.geometry("600x400")

    tree_report = ttk.Treeview(
        report_window,
        columns=("Name", "Marks", "Grade"),
        show="headings"
    )

    tree_report.heading("Name", text="Student Name")
    tree_report.heading("Marks", text="Marks")
    tree_report.heading("Grade", text="Grade")

    tree_report.column("Name", width=250)
    tree_report.column("Marks", width=120)
    tree_report.column("Grade", width=120)

    tree_report.pack(fill="both", expand=True, padx=10, pady=10)

    data = get_performance_report()

    for student in data:

        name = student[0]
        marks = student[1]

        if marks >= 90:
            grade = "A"

        elif marks >= 75:
            grade = "B"

        elif marks >= 60:
            grade = "C"

        else:
            grade = "D"

        tree_report.insert(
            "",
            tk.END,
            values=(name, marks, grade)
        )

def student_report():

    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a student first."
        )
        return

    values = tree.item(selected, "values")

    student_id = values[0]
    name = values[1]
    course = values[2]
    marks = float(values[3])
    attendance = float(values[4])

    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    else:
        grade = "D"

    report_window = tk.Toplevel(root)
    report_window.title("Student Report")
    report_window.geometry("500x350")

    tk.Label(
        report_window,
        text="STUDENT REPORT",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    info = f"""
Student ID : {student_id}

Name       : {name}

Course     : {course}

Marks      : {marks}

Grade      : {grade}

Attendance : {attendance}%
"""

    tk.Label(
        report_window,
        text=info,
        justify="left",
        font=("Arial", 12)
    ).pack(padx=20, pady=10)

def attendance_report():

    report_window = tk.Toplevel(root)
    report_window.title("Attendance Report")
    report_window.geometry("650x400")

    tree_report = ttk.Treeview(
        report_window,
        columns=("Name", "Attendance", "Status"),
        show="headings"
    )

    tree_report.heading("Name", text="Student Name")
    tree_report.heading("Attendance", text="Attendance (%)")
    tree_report.heading("Status", text="Status")

    tree_report.column("Name", width=250)
    tree_report.column("Attendance", width=150)
    tree_report.column("Status", width=150)

    tree_report.pack(fill="both", expand=True, padx=10, pady=10)

    students = get_all_students()

    for student in students:

        name = student[1]
        attendance = float(student[4])

        if attendance >= 75:
            status = "Good"

        elif attendance >= 50:
            status = "Warning"

        else:
            status = "Critical"

        tree_report.insert(
            "",
            tk.END,
            values=(name, attendance, status)
        )
# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x900")
root.configure(bg="#f4f6f9")

# ---------------- TITLE ---------------- #

title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#f4f6f9",
    fg="#2c3e50"
)

title.pack(pady=20)

# ---------------- FORM ---------------- #

form_frame = tk.LabelFrame(
    root,
    text="Student Details",
    padx=20,
    pady=20
)

form_frame.pack(pady=10)

# Student ID

tk.Label(
    form_frame,
    text="Student ID"
).grid(row=0, column=0, padx=10, pady=10)

id_entry = tk.Entry(form_frame, width=30)
id_entry.grid(row=0, column=1)

# Name

tk.Label(
    form_frame,
    text="Name"
).grid(row=1, column=0, padx=10, pady=10)

name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=1, column=1)

# Course

tk.Label(
    form_frame,
    text="Course"
).grid(row=2, column=0, padx=10, pady=10)

course_combo = ttk.Combobox(
    form_frame,
    values=[
        "BCA",
        "MCA",
        "B.Tech",
        "M.Tech",
        "B.Sc",
        "M.Sc"
    ],
    width=27
)

course_combo.grid(row=2, column=1)

# Marks

tk.Label(
    form_frame,
    text="Marks"
).grid(row=3, column=0, padx=10, pady=10)

marks_entry = tk.Entry(form_frame, width=30)
marks_entry.grid(row=3, column=1)

# Attendance

tk.Label(
    form_frame,
    text="Attendance (%)"
).grid(row=4, column=0, padx=10, pady=10)

attendance_entry = tk.Entry(form_frame, width=30)
attendance_entry.grid(row=4, column=1)

# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(root, bg="#f4f6f9")
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=save_student
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Update Student",
    width=15,
    command=update_selected_student
).grid(row=0, column=1, padx=10)

tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_selected_student
).grid(row=0, column=2, padx=10)

tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
).grid(row=0, column=3, padx=10)






# ---------------- SEARCH ---------------- #

search_frame = tk.Frame(root, bg="#f4f6f9")
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search Student:",
    bg="#f4f6f9"
).pack(side="left")

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=10)

tk.Button(
    search_frame,
    text="Search",
    command=search_student_record
).pack(side="left")


# ---------------- REPORTS ---------------- #

report_frame = tk.Frame(root, bg="#f4f6f9")
report_frame.pack(pady=10)

tk.Button(
    report_frame,
    text="Student Report",
    width=20,
    command=student_report
).grid(row=0, column=0, padx=20)

tk.Button(
    report_frame,
    text="Performance Report",
    width=20,
    command=performance_report
).grid(row=0, column=1, padx=20)

tk.Button(
    report_frame,
    text="Attendance Report",
    width=20,
    command=attendance_report
).grid(row=0, column=2, padx=20)


# ---------------- TABLE ---------------- #

table_frame = tk.Frame(root)
table_frame.pack(pady=20)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Course",
        "Marks",
        "Attendance"
    ),
    show="headings",
    height=8
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Course", text="Course")
tree.heading("Marks", text="Marks")
tree.heading("Attendance", text="Attendance")

tree.column("ID", width=150)
tree.column("Name", width=250)
tree.column("Course", width=150)
tree.column("Marks", width=120)
tree.column("Attendance", width=150)

tree.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.config(
    command=tree.yview
)

tree.pack()

tree.bind(
    "<ButtonRelease-1>",
    select_student
)


# ---------------- LOAD DATA ---------------- #

load_students()


# ---------------- START APP ---------------- #

root.mainloop()