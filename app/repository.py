"""In-memory records with relationship and access checks for Gradebook."""

from decimal import Decimal
from itertools import count
from threading import RLock

from app.grading import AssessmentGrade, calculate_weighted_average
from app.models import Assessment, Course, Enrollment, Grade, Role, User


class InMemoryGradebookRepository:
    """Store one process's records; actor IDs must come from trusted login code.

    Account provisioning is internal. Future HTTP routes must obtain actor_id
    from the authenticated session, never from client-supplied ownership fields.
    """

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._courses: dict[int, Course] = {}
        self._assessments: dict[int, Assessment] = {}
        self._enrollments: dict[tuple[int, int], Enrollment] = {}
        self._grades: dict[tuple[int, int], Grade] = {}
        self._user_ids = count(1)
        self._course_ids = count(1)
        self._assessment_ids = count(1)
        self._lock = RLock()

    def healthy(self) -> bool:
        """In-memory storage has no external database to check."""
        return True

    def create_user(
        self, username: str, role: Role, password_hash: str, *, if_missing: bool = False
    ) -> User:
        """Provision a pre-created account internally; not a public registration API."""
        with self._lock:
            for user in self._users.values():
                if user.username == username:
                    if not if_missing:
                        raise ValueError("Username already exists")
                    if user.role != role:
                        raise ValueError("Existing demo account has a different role")
                    return user
            user = User(next(self._user_ids), username, role, password_hash)
            self._users[user.id] = user
            return user

    def create_course(self, actor_id: int, name: str) -> Course:
        with self._lock:
            actor = self._user(actor_id)
            if actor.role != Role.LECTURER:
                raise PermissionError("Only lecturers can create courses")
            course = Course(next(self._course_ids), name, actor.id)
            self._courses[course.id] = course
            return course

    def get_user(self, user_id: int) -> User:
        """Resolve a trusted session ID internally."""
        with self._lock:
            return self._user(user_id)

    def find_user_by_username(self, username: str) -> User | None:
        """Look up an exact, case-sensitive username for internal login handling."""
        with self._lock:
            return next((user for user in self._users.values() if user.username == username), None)

    def list_courses(self, actor_id: int) -> list[Course]:
        with self._lock:
            actor = self._user(actor_id)
            if actor.role == Role.LECTURER:
                return [
                    course for course in self._courses.values() if course.lecturer_id == actor.id
                ]
            return [
                course
                for course in self._courses.values()
                if (course.id, actor.id) in self._enrollments
            ]

    def create_assessment(
        self, actor_id: int, course_id: int, name: str, weight: Decimal
    ) -> Assessment:
        with self._lock:
            course = self._owned_course(actor_id, course_id)
            assessment = Assessment(next(self._assessment_ids), course.id, name, weight)
            self._assessments[assessment.id] = assessment
            return assessment

    def list_assessments(self, actor_id: int, course_id: int) -> list[Assessment]:
        with self._lock:
            course = self._visible_course(actor_id, course_id)
            return [item for item in self._assessments.values() if item.course_id == course.id]

    def enroll_student(self, actor_id: int, course_id: int, student_id: int) -> Enrollment:
        with self._lock:
            course = self._owned_course(actor_id, course_id)
            student = self._user(student_id)
            if student.role != Role.STUDENT:
                raise ValueError("Only student accounts can be enrolled")
            key = (course.id, student.id)
            if key not in self._enrollments:
                self._enrollments[key] = Enrollment(course.id, student.id)
            return self._enrollments[key]

    def list_enrollments(self, actor_id: int, course_id: int) -> list[Enrollment]:
        with self._lock:
            course = self._owned_course(actor_id, course_id)
            return [item for item in self._enrollments.values() if item.course_id == course.id]

    def set_grade(
        self, actor_id: int, assessment_id: int, student_id: int, value: Decimal
    ) -> Grade:
        """Create or replace the grade for the assessment/student pair."""
        with self._lock:
            assessment = self._assessment(assessment_id)
            course = self._owned_course(actor_id, assessment.course_id)
            student = self._enrolled_student(course.id, student_id)
            grade = Grade(assessment.id, student.id, value)
            self._grades[(assessment.id, student.id)] = grade
            return grade

    def get_grades(self, actor_id: int, course_id: int, student_id: int) -> list[Grade]:
        with self._lock:
            self._authorize_result_access(actor_id, course_id, student_id)
            return [
                grade
                for grade in self._grades.values()
                if grade.student_id == student_id
                and self._assessments[grade.assessment_id].course_id == course_id
            ]

    def get_average(self, actor_id: int, course_id: int, student_id: int) -> Decimal | None:
        return self.get_result(actor_id, course_id, student_id)[1]

    def get_result(
        self, actor_id: int, course_id: int, student_id: int
    ) -> tuple[list[Grade], Decimal | None]:
        """Read grades and their weighted average together."""
        with self._lock:
            grades = self.get_grades(actor_id, course_id, student_id)
            grades_by_assessment = {grade.assessment_id: grade.value for grade in grades}
            inputs = [
                AssessmentGrade(grades_by_assessment.get(assessment.id), assessment.weight)
                for assessment in self._assessments.values()
                if assessment.course_id == course_id
            ]
            return grades, calculate_weighted_average(inputs)

    def _user(self, user_id: int) -> User:
        # Reject bool/float aliases: Python dictionary keys True and 1 are equal.
        user = self._users.get(user_id) if type(user_id) is int else None
        if user is None:
            raise LookupError("User not found")
        return user

    def _course(self, course_id: int) -> Course:
        course = self._courses.get(course_id) if type(course_id) is int else None
        if course is None:
            raise LookupError("Course not found")
        return course

    def _assessment(self, assessment_id: int) -> Assessment:
        assessment = self._assessments.get(assessment_id) if type(assessment_id) is int else None
        if assessment is None:
            raise LookupError("Assessment not found")
        return assessment

    def _owned_course(self, actor_id: int, course_id: int) -> Course:
        actor = self._user(actor_id)
        if actor.role != Role.LECTURER:
            raise PermissionError("Only lecturers can manage courses")
        course = self._course(course_id)
        if course.lecturer_id != actor.id:
            raise PermissionError("Course belongs to another lecturer")
        return course

    def _visible_course(self, actor_id: int, course_id: int) -> Course:
        actor = self._user(actor_id)
        course = self._course(course_id)
        if actor.role == Role.LECTURER:
            if course.lecturer_id != actor.id:
                raise PermissionError("Course belongs to another lecturer")
        elif (course.id, actor.id) not in self._enrollments:
            raise PermissionError("Student is not enrolled in this course")
        return course

    def _enrolled_student(self, course_id: int, student_id: int) -> User:
        student = self._user(student_id)
        if student.role != Role.STUDENT:
            raise ValueError("Account must be a student")
        if (course_id, student.id) not in self._enrollments:
            raise ValueError("Student must be enrolled before grades can be accessed")
        return student

    def _authorize_result_access(self, actor_id: int, course_id: int, student_id: int) -> None:
        actor = self._user(actor_id)
        self._visible_course(actor.id, course_id)
        if actor.role == Role.STUDENT and actor.id != student_id:
            raise PermissionError("Students can only read their own results")
        self._enrolled_student(course_id, student_id)
