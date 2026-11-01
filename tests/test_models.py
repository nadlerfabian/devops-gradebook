"""Verify record validation and its use with the existing grading rules."""

from decimal import Decimal

import pytest

from app.grading import AssessmentGrade, calculate_weighted_average
from app.models import Assessment, Course, Enrollment, Grade, Role, User


def test_course_records_supply_grades_and_weights_for_a_student_result():
    # These model-test placeholders are not usable password hashes or accounts.
    lecturer = User(1, "demo-lecturer", Role.LECTURER, "model-test-placeholder")
    student = User(2, "demo-student", Role.STUDENT, "model-test-placeholder")
    course = Course(1, "DevOps", lecturer.id)
    enrollment = Enrollment(course.id, student.id)
    project = Assessment(1, course.id, "Project", Decimal("40"))
    exam = Assessment(2, course.id, "Exam", Decimal("60"))
    project_grade = Grade(project.id, student.id, Decimal("5.0"))
    exam_grade = Grade(exam.id, student.id, Decimal("4.0"))

    result = calculate_weighted_average(
        [
            AssessmentGrade(project_grade.value, project.weight),
            AssessmentGrade(exam_grade.value, exam.weight),
        ]
    )

    assert enrollment.student_id == project_grade.student_id == exam_grade.student_id
    assert str(result) == "4.40"


def test_user_representation_does_not_expose_password_hash():
    user = User(1, "demo-student", Role.STUDENT, "model-test-private-value")

    assert "demo-student" in repr(user)
    assert "model-test-private-value" not in repr(user)


@pytest.mark.parametrize("role", ["admin", "student", None])
def test_user_requires_an_explicit_supported_role(role):
    with pytest.raises(ValueError, match="Role"):
        User(1, "demo-student", role, "model-test-placeholder")


@pytest.mark.parametrize("value", ["", "   ", None])
@pytest.mark.parametrize("field", ["username", "password_hash"])
def test_account_fields_cannot_be_blank(value, field):
    username = value if field == "username" else "demo-student"
    password_hash = value if field == "password_hash" else "model-test-placeholder"

    with pytest.raises(ValueError, match="nonempty text"):
        User(1, username, Role.STUDENT, password_hash)


@pytest.mark.parametrize("name", ["", "   ", None])
def test_course_and_assessment_names_cannot_be_blank(name):
    with pytest.raises(ValueError, match="Course name"):
        Course(1, name, 1)
    with pytest.raises(ValueError, match="Assessment name"):
        Assessment(1, 1, name, Decimal("40"))


@pytest.mark.parametrize("invalid_id", [0, -1, True, "1"])
def test_relationship_ids_must_be_positive_integers(invalid_id):
    with pytest.raises(ValueError, match="Lecturer ID"):
        Course(1, "DevOps", invalid_id)
    with pytest.raises(ValueError, match="Course ID"):
        Assessment(1, invalid_id, "Project", Decimal("40"))
    with pytest.raises(ValueError, match="Student ID"):
        Enrollment(1, invalid_id)
    with pytest.raises(ValueError, match="Assessment ID"):
        Grade(invalid_id, 2, Decimal("5"))


def test_record_ids_must_be_positive():
    with pytest.raises(ValueError, match="User ID"):
        User(0, "demo-student", Role.STUDENT, "model-test-placeholder")
    with pytest.raises(ValueError, match="Course ID"):
        Course(0, "DevOps", 1)
    with pytest.raises(ValueError, match="Assessment ID"):
        Assessment(0, 1, "Project", Decimal("40"))


@pytest.mark.parametrize("value", ["0.99", "6.01", "4.755", "NaN"])
def test_grade_records_use_the_existing_grade_validation(value):
    with pytest.raises(ValueError, match="Grade"):
        Grade(1, 2, Decimal(value))


@pytest.mark.parametrize("value", ["0", "-1", "Infinity"])
def test_assessments_use_the_existing_weight_validation(value):
    with pytest.raises(ValueError, match="Weight"):
        Assessment(1, 1, "Project", Decimal(value))


def test_partial_weight_configuration_is_a_valid_assessment():
    assessment = Assessment(1, 1, "Project", Decimal("40"))

    assert calculate_weighted_average([AssessmentGrade(Decimal("5"), assessment.weight)]) is None
