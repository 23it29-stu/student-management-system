import mysql.connector
from config import *

def connect_db():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def add_student(student_id, name, course, marks, attendance):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO students
    (student_id, name, course, marks, attendance)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        student_id,
        name,
        course,
        marks,
        attendance
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()


def get_all_students():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return students

def update_student(student_id, name, course, marks, attendance):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    UPDATE students
    SET name=%s,
        course=%s,
        marks=%s,
        attendance=%s
    WHERE student_id=%s
    """

    values = (
        name,
        course,
        marks,
        attendance,
        student_id
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

def delete_student(student_id):

    conn = connect_db()
    cursor = conn.cursor()

    query = "DELETE FROM students WHERE student_id = %s"

    cursor.execute(query, (student_id,))

    conn.commit()

    cursor.close()
    conn.close()

def search_student(name):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM students
    WHERE name LIKE %s
    """

    cursor.execute(query, ("%" + name + "%",))

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return students

def get_performance_report():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, marks FROM students"
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data