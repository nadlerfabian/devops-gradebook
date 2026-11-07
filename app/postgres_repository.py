"""PostgreSQL storage using the same records and grading rules as memory storage."""

from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from app.grading import AssessmentGrade, calculate_weighted_average
from app.models import Assessment, Course, Enrollment, Grade, Role, User


class PostgresGradebookRepository:
    def __init__(self, database_url):
        self._database_url = database_url

    def _connect(self):
        return psycopg.connect(self._database_url, connect_timeout=3, row_factory=dict_row)

    def initialize(self):
        """Create the initial schema, one startup transaction at a time."""
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        with self._connect() as conn:
            conn.execute("SELECT pg_advisory_xact_lock(674211)")
            conn.execute(schema)

    def healthy(self):
        with self._connect() as conn:
            conn.execute("SELECT 1 FROM users LIMIT 1")
        return True

    def create_user(self, username, role, password_hash, *, if_missing=False):
        User(1, username, role, password_hash)
        with self._connect() as conn:
            row = conn.execute(
                """INSERT INTO users (username, role, password_hash) VALUES (%s, %s, %s)
                   ON CONFLICT (username) DO NOTHING RETURNING *""",
                (username, role.value, password_hash),
            ).fetchone()
            if row is None:
                if not if_missing:
                    raise ValueError("Username already exists")
                row = conn.execute(
                    "SELECT * FROM users WHERE username = %s", (username,)
                ).fetchone()
                if row["role"] != role.value:
                    raise ValueError("Existing demo account has a different role")
            return self._user_record(row)

    @staticmethod
    def _user_record(row):
        return User(row["id"], row["username"], Role(row["role"]), row["password_hash"])

    def _user(self, conn, user_id):
        if type(user_id) is not int or not 0 < user_id < 2**63:
            raise LookupError("User not found")
        row = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,)).fetchone()
        if row is None:
            raise LookupError("User not found")
        return self._user_record(row)

    def get_user(self, user_id):
        with self._connect() as conn:
            return self._user(conn, user_id)

    def find_user_by_username(self, username):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE username = %s", (username,)).fetchone()
            return self._user_record(row) if row is not None else None

    def _lecturer(self, conn, actor_id):
        actor = self._user(conn, actor_id)
        if actor.role != Role.LECTURER:
            raise PermissionError("Only lecturers can manage courses")
        return actor

    def _course(self, conn, course_id):
        if type(course_id) is not int or not 0 < course_id < 2**63:
            raise LookupError("Course not found")
        row = conn.execute("SELECT * FROM courses WHERE id = %s", (course_id,)).fetchone()
        if row is None:
            raise LookupError("Course not found")
        return Course(**row)

    def _owned_course(self, conn, actor_id, course_id):
        lecturer = self._lecturer(conn, actor_id)
        course = self._course(conn, course_id)
        if course.lecturer_id != lecturer.id:
            raise PermissionError("Course belongs to another lecturer")
        return course

    @staticmethod
    def _is_enrolled(conn, course_id, student_id):
        return (
            conn.execute(
                "SELECT 1 FROM enrollments WHERE course_id = %s AND student_id = %s",
                (course_id, student_id),
            ).fetchone()
            is not None
        )

    def _visible_course(self, conn, actor, course_id):
        course = self._course(conn, course_id)
        if actor.role == Role.LECTURER:
            if course.lecturer_id != actor.id:
                raise PermissionError("Course belongs to another lecturer")
        elif not self._is_enrolled(conn, course.id, actor.id):
            raise PermissionError("Student is not enrolled in this course")
        return course

    def _enrolled_student(self, conn, course_id, student_id):
        student = self._user(conn, student_id)
        if student.role != Role.STUDENT:
            raise ValueError("Account must be a student")
        if not self._is_enrolled(conn, course_id, student.id):
            raise ValueError("Student must be enrolled before grades can be accessed")
        return student

    def create_course(self, actor_id, name):
        with self._connect() as conn:
            lecturer = self._lecturer(conn, actor_id)
            Course(1, name, lecturer.id)
            row = conn.execute(
                "INSERT INTO courses (name, lecturer_id) VALUES (%s, %s) RETURNING *",
                (name, lecturer.id),
            ).fetchone()
            return Course(**row)

    def list_courses(self, actor_id):
        with self._connect() as conn:
            actor = self._user(conn, actor_id)
            if actor.role == Role.LECTURER:
                rows = conn.execute(
                    "SELECT * FROM courses WHERE lecturer_id = %s ORDER BY id", (actor.id,)
                )
            else:
                rows = conn.execute(
                    """SELECT courses.* FROM courses JOIN enrollments
                       ON courses.id = enrollments.course_id
                       WHERE enrollments.student_id = %s ORDER BY courses.id""",
                    (actor.id,),
                )
            return [Course(**row) for row in rows]

    def create_assessment(self, actor_id, course_id, name, weight):
        with self._connect() as conn:
            course = self._owned_course(conn, actor_id, course_id)
            Assessment(1, course.id, name, weight)
            row = conn.execute(
                """INSERT INTO assessments (course_id, name, weight)
                   VALUES (%s, %s, %s) RETURNING *""",
                (course.id, name, weight),
            ).fetchone()
            return Assessment(**row)

    def list_assessments(self, actor_id, course_id):
        with self._connect() as conn:
            course = self._visible_course(conn, self._user(conn, actor_id), course_id)
            rows = conn.execute(
                "SELECT * FROM assessments WHERE course_id = %s ORDER BY id", (course.id,)
            )
            return [Assessment(**row) for row in rows]

    def enroll_student(self, actor_id, course_id, student_id):
        with self._connect() as conn:
            course = self._owned_course(conn, actor_id, course_id)
            student = self._user(conn, student_id)
            if student.role != Role.STUDENT:
                raise ValueError("Only student accounts can be enrolled")
            conn.execute(
                """INSERT INTO enrollments (course_id, student_id) VALUES (%s, %s)
                   ON CONFLICT (course_id, student_id) DO NOTHING""",
                (course.id, student.id),
            )
            return Enrollment(course.id, student.id)

    def list_enrollments(self, actor_id, course_id):
        with self._connect() as conn:
            course = self._owned_course(conn, actor_id, course_id)
            rows = conn.execute(
                "SELECT * FROM enrollments WHERE course_id = %s ORDER BY student_id", (course.id,)
            )
            return [Enrollment(**row) for row in rows]

    def set_grade(self, actor_id, assessment_id, student_id, value):
        if type(assessment_id) is not int or not 0 < assessment_id < 2**63:
            raise LookupError("Assessment not found")
        with self._connect() as conn:
            row = conn.execute(
                "SELECT course_id FROM assessments WHERE id = %s", (assessment_id,)
            ).fetchone()
            if row is None:
                raise LookupError("Assessment not found")
            course = self._owned_course(conn, actor_id, row["course_id"])
            student = self._enrolled_student(conn, course.id, student_id)
            grade = Grade(assessment_id, student.id, value)
            conn.execute(
                """INSERT INTO grades (assessment_id, student_id, course_id, value)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (assessment_id, student_id)
                   DO UPDATE SET value = EXCLUDED.value""",
                (grade.assessment_id, grade.student_id, course.id, grade.value),
            )
            return grade

    def get_grades(self, actor_id, course_id, student_id):
        return self.get_result(actor_id, course_id, student_id)[0]

    def get_average(self, actor_id, course_id, student_id):
        return self.get_result(actor_id, course_id, student_id)[1]

    def get_result(self, actor_id, course_id, student_id):
        with self._connect() as conn:
            actor = self._user(conn, actor_id)
            course = self._visible_course(conn, actor, course_id)
            if actor.role == Role.STUDENT and actor.id != student_id:
                raise PermissionError("Students can only read their own results")
            student = self._enrolled_student(conn, course.id, student_id)
            rows = conn.execute(
                """SELECT assessments.id, assessments.weight, grades.value
                   FROM assessments LEFT JOIN grades ON assessments.id = grades.assessment_id
                   AND grades.student_id = %s
                   WHERE assessments.course_id = %s ORDER BY assessments.id""",
                (student.id, course.id),
            ).fetchall()
        grades = [
            Grade(row["id"], student.id, row["value"]) for row in rows if row["value"] is not None
        ]
        inputs = [AssessmentGrade(row["value"], row["weight"]) for row in rows]
        return grades, calculate_weighted_average(inputs)
