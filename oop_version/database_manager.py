import mysql.connector


class DatabaseConnectionError(Exception):
    pass


class DatabaseManager:

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="student_admin",
                password="Student@123",
                database="student_management",
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as exc:
            raise DatabaseConnectionError(
                "Unable to connect to the student_management database. "
                "Check MySQL is running and the credentials/table exist."
            ) from exc

    def _execute(self, query, values=None):
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
        except mysql.connector.Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Database operation failed: {exc}") from exc

    def add_student(self, student):

        query = """
        INSERT INTO students
        (student_id, name, course, marks, attendance)
        VALUES (%s, %s, %s, %s, %s)
        """

        self._execute(query, student.to_tuple())
        self.connection.commit()

    def get_all_students(self):

        query = """
        SELECT *
        FROM students
        """

        self._execute(query)

        return self.cursor.fetchall()

    def delete_student(self, student_id):

        query = """
        DELETE FROM students
        WHERE student_id = %s
        """

        self._execute(query, (student_id,))
        self.connection.commit()

    def update_student(self, student):

        query = """
        UPDATE students
        SET
        name=%s,
        course=%s,
        marks=%s,
        attendance=%s
        WHERE student_id=%s
        """

        self._execute(
            query,
            (
                student.name,
                student.course,
                student.marks,
                student.attendance,
                student.student_id,
            ),
        )
        self.connection.commit()

    def search_student(self, keyword):

        query = """
        SELECT *
        FROM students
        WHERE
        student_id LIKE %s
        OR name LIKE %s
        """

        search_value = f"%{keyword}%"

        self._execute(
            query,
            (
                search_value,
                search_value,
            ),
        )

        return self.cursor.fetchall()

    def close(self):
        try:
            self.cursor.close()
        finally:
            self.connection.close()