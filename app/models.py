"""Validated records; storage will enforce relationships and permissions."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum

from app.grading import validate_grade, validate_weight


def _require_positive_id(value: int, name: str) -> None:
    """IDs must be positive integers, not booleans or numeric strings."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _require_nonempty_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")


class Role(StrEnum):
    """The two supported account roles."""

    LECTURER = "lecturer"
    STUDENT = "student"


@dataclass(frozen=True)
class User:
    """An account; a student user's ID also identifies their student record."""

    id: int
    username: str
    role: Role
    password_hash: str = field(repr=False)

    def __post_init__(self) -> None:
        _require_positive_id(self.id, "User ID")
        _require_nonempty_text(self.username, "Username")
        _require_nonempty_text(self.password_hash, "Password hash")
        if not isinstance(self.role, Role):
            raise ValueError("Role must be Role.LECTURER or Role.STUDENT")


@dataclass(frozen=True)
class Course:
    """A course owned by a lecturer."""

    id: int
    name: str
    lecturer_id: int

    def __post_init__(self) -> None:
        _require_positive_id(self.id, "Course ID")
        _require_nonempty_text(self.name, "Course name")
        _require_positive_id(self.lecturer_id, "Lecturer ID")


@dataclass(frozen=True)
class Assessment:
    """A course assessment whose percentage weight applies to all students."""

    id: int
    course_id: int
    name: str
    weight: Decimal

    def __post_init__(self) -> None:
        _require_positive_id(self.id, "Assessment ID")
        _require_positive_id(self.course_id, "Course ID")
        _require_nonempty_text(self.name, "Assessment name")
        validate_weight(self.weight)


@dataclass(frozen=True)
class Enrollment:
    """A link from a student account to a course."""

    course_id: int
    student_id: int

    def __post_init__(self) -> None:
        _require_positive_id(self.course_id, "Course ID")
        _require_positive_id(self.student_id, "Student ID")


@dataclass(frozen=True)
class Grade:
    """One recorded grade, identified by its assessment/student pair."""

    assessment_id: int
    student_id: int
    value: Decimal

    def __post_init__(self) -> None:
        _require_positive_id(self.assessment_id, "Assessment ID")
        _require_positive_id(self.student_id, "Student ID")
        validate_grade(self.value)
