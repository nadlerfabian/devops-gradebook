"""Exercise storage behavior, relationships, and access boundaries."""

import os
from decimal import Decimal
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql
from psycopg.conninfo import make_conninfo

from app import create_app
from app.models import Role
from app.postgres_repository import PostgresGradebookRepository
from app.repository import InMemoryGradebookRepository


@pytest.fixture
def postgres_url():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to run PostgreSQL integration tests")

    schema = f"gradebook_test_{uuid4().hex}"
    with psycopg.connect(url) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    try:
        yield make_conninfo(url, options=f"-c search_path={schema}")
    finally:
        with psycopg.connect(url) as conn:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


@pytest.fixture(params=["memory", "postgres"])
def setup(request):
    if request.param == "postgres":
        repo = PostgresGradebookRepository(request.getfixturevalue("postgres_url"))
        repo.initialize()
    else:
        repo = InMemoryGradebookRepository()
    # Model placeholders are not real password hashes or usable credentials.
    owner = repo.create_user("lecturer-a", Role.LECTURER, "test-placeholder")
    outsider = repo.create_user("lecturer-b", Role.LECTURER, "test-placeholder")
    student = repo.create_user("student-a", Role.STUDENT, "test-placeholder")
    peer = repo.create_user("student-b", Role.STUDENT, "test-placeholder")
    course = repo.create_course(owner.id, "DevOps")
    project = repo.create_assessment(owner.id, course.id, "Project", Decimal("40"))
    exam = repo.create_assessment(owner.id, course.id, "Exam", Decimal("60"))
    repo.enroll_student(owner.id, course.id, student.id)
    return repo, owner, outsider, student, peer, course, project, exam


def test_postgres_survives_app_restart(postgres_url, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", postgres_url)
    config = {
        "TESTING": True,
        "SECRET_KEY": "test-only",
        "DEMO_LECTURER_PASSWORD": "synthetic-lecturer-password",
        "DEMO_STUDENT_PASSWORD": "synthetic-student-password",
    }
    first = create_app(config=config)
    repo = first.extensions["repository"]
    owner = repo.find_user_by_username("lecturer")
    student = repo.find_user_by_username("student")
    course = repo.create_course(owner.id, "DevOps")
    assessment = repo.create_assessment(owner.id, course.id, "Project", Decimal("100"))
    repo.enroll_student(owner.id, course.id, student.id)
    repo.set_grade(owner.id, assessment.id, student.id, Decimal("5.25"))

    second = create_app(config=config)
    new_repo = second.extensions["repository"]
    assert new_repo.find_user_by_username("student") == student
    assert new_repo.get_user(owner.id) == owner
    assert second.test_client().get("/ready").status_code == 200
    assert second.test_client().get("/health").status_code == 200
    client = second.test_client()
    with client.session_transaction() as session:
        session["user_id"] = student.id
    result = client.get(f"/api/courses/{course.id}/results/{student.id}")
    assert result.status_code == 200
    assert result.get_json()["average"] == "5.25"


def test_enrollment_grading_and_correction_recalculate_result(setup):
    repo, owner, _, student, _, course, project, exam = setup
    repo.set_grade(owner.id, project.id, student.id, Decimal("5"))
    assert repo.get_average(student.id, course.id, student.id) is None

    repo.set_grade(owner.id, exam.id, student.id, Decimal("4"))
    assert str(repo.get_average(student.id, course.id, student.id)) == "4.40"
    assert str(repo.get_average(owner.id, course.id, student.id)) == "4.40"

    repo.set_grade(owner.id, exam.id, student.id, Decimal("5"))
    assert len(repo.get_grades(owner.id, course.id, student.id)) == 2
    assert str(repo.get_average(student.id, course.id, student.id)) == "5.00"


def test_duplicate_usernames_are_rejected_without_replacing_account(setup):
    repo, owner, _, _, _, _, _, _ = setup

    with pytest.raises(ValueError, match="Username already exists"):
        repo.create_user(owner.username, Role.STUDENT, "another-placeholder")
    assert repo.list_courses(owner.id)[0].lecturer_id == owner.id


def test_duplicate_enrollment_is_idempotent(setup):
    repo, owner, _, student, _, course, _, _ = setup
    first = repo.enroll_student(owner.id, course.id, student.id)
    second = repo.enroll_student(owner.id, course.id, student.id)

    assert first == second
    assert repo.list_enrollments(owner.id, course.id) == [first]


def test_courses_and_assessments_are_visible_only_to_authorized_users(setup):
    repo, owner, outsider, student, peer, course, project, exam = setup

    assert repo.list_courses(owner.id) == [course]
    assert repo.list_courses(student.id) == [course]
    assert repo.list_courses(outsider.id) == []
    assert repo.list_courses(peer.id) == []
    assert repo.list_assessments(student.id, course.id) == [project, exam]
    with pytest.raises(PermissionError, match="another lecturer"):
        repo.list_assessments(outsider.id, course.id)
    with pytest.raises(PermissionError, match="not enrolled"):
        repo.list_assessments(peer.id, course.id)


@pytest.mark.parametrize("actor_kind", ["student", "outsider"])
def test_unauthorized_users_cannot_change_course_data(setup, actor_kind):
    repo, owner, outsider, student, peer, course, project, _ = setup
    actor = student if actor_kind == "student" else outsider

    with pytest.raises(PermissionError):
        repo.create_assessment(actor.id, course.id, "Unauthorized", Decimal("100"))
    with pytest.raises(PermissionError):
        repo.enroll_student(actor.id, course.id, peer.id)
    with pytest.raises(PermissionError):
        repo.set_grade(actor.id, project.id, student.id, Decimal("6"))
    with pytest.raises(PermissionError):
        repo.list_enrollments(actor.id, course.id)
    assert len(repo.list_assessments(owner.id, course.id)) == 2
    assert repo.get_grades(owner.id, course.id, student.id) == []


def test_students_cannot_create_courses(setup):
    repo, _, _, student, _, _, _, _ = setup

    with pytest.raises(PermissionError, match="Only lecturers"):
        repo.create_course(student.id, "Unauthorized")


def test_course_requires_an_existing_owner_and_assessment_requires_a_course(setup):
    repo, owner, _, _, _, _, _, _ = setup

    with pytest.raises(LookupError, match="User not found"):
        repo.create_course(999, "Unknown owner")
    with pytest.raises(LookupError, match="Course not found"):
        repo.create_assessment(owner.id, 999, "Unknown course", Decimal("100"))


def test_only_existing_student_accounts_can_be_enrolled(setup):
    repo, owner, outsider, _, _, course, _, _ = setup

    with pytest.raises(ValueError, match="Only student accounts"):
        repo.enroll_student(owner.id, course.id, outsider.id)
    with pytest.raises(LookupError, match="User not found"):
        repo.enroll_student(owner.id, course.id, 999)


def test_grades_require_an_existing_assessment_and_enrolled_student(setup):
    repo, owner, outsider, student, peer, _, project, _ = setup

    with pytest.raises(LookupError, match="Assessment not found"):
        repo.set_grade(owner.id, 999, student.id, Decimal("5"))
    with pytest.raises(ValueError, match="must be enrolled"):
        repo.set_grade(owner.id, project.id, peer.id, Decimal("5"))
    with pytest.raises(ValueError, match="must be a student"):
        repo.set_grade(owner.id, project.id, outsider.id, Decimal("5"))


def test_students_cannot_read_peer_results_and_other_lecturers_cannot_read_results(setup):
    repo, owner, outsider, student, peer, course, project, _ = setup
    repo.enroll_student(owner.id, course.id, peer.id)
    repo.set_grade(owner.id, project.id, student.id, Decimal("5"))

    with pytest.raises(PermissionError, match="own results"):
        repo.get_average(peer.id, course.id, student.id)
    with pytest.raises(PermissionError, match="another lecturer"):
        repo.get_grades(outsider.id, course.id, student.id)
    assert repo.get_grades(peer.id, course.id, peer.id) == []


def test_course_owner_cannot_read_results_for_a_non_enrolled_student(setup):
    repo, owner, _, _, peer, course, _, _ = setup

    with pytest.raises(ValueError, match="must be enrolled"):
        repo.get_average(owner.id, course.id, peer.id)


def test_grade_lists_do_not_mix_courses_or_students(setup):
    repo, owner, _, student, peer, course, project, _ = setup
    repo.enroll_student(owner.id, course.id, peer.id)
    other_course = repo.create_course(owner.id, "Other course")
    repo.enroll_student(owner.id, other_course.id, student.id)
    other_exam = repo.create_assessment(owner.id, other_course.id, "Exam", Decimal("100"))
    expected = repo.set_grade(owner.id, project.id, student.id, Decimal("5"))
    repo.set_grade(owner.id, project.id, peer.id, Decimal("1"))
    repo.set_grade(owner.id, other_exam.id, student.id, Decimal("6"))

    assert repo.get_grades(student.id, course.id, student.id) == [expected]
    assert str(repo.get_average(student.id, other_course.id, student.id)) == "6.00"


def test_invalid_correction_does_not_overwrite_existing_grade(setup):
    repo, owner, _, student, _, course, project, _ = setup
    original = repo.set_grade(owner.id, project.id, student.id, Decimal("5"))

    with pytest.raises(ValueError, match="Grade must be between"):
        repo.set_grade(owner.id, project.id, student.id, Decimal("7"))
    assert repo.get_grades(student.id, course.id, student.id) == [original]


def test_incomplete_weights_and_empty_course_do_not_produce_a_final_grade(setup):
    repo, owner, _, student, _, _, _, _ = setup
    course = repo.create_course(owner.id, "Work in progress")
    repo.enroll_student(owner.id, course.id, student.id)
    assert repo.get_average(student.id, course.id, student.id) is None

    assessment = repo.create_assessment(owner.id, course.id, "Project", Decimal("40"))
    repo.set_grade(owner.id, assessment.id, student.id, Decimal("5"))
    assert repo.get_average(student.id, course.id, student.id) is None


@pytest.mark.parametrize("invalid_id", [True, 1.0, "1", 0, -1])
def test_invalid_id_types_cannot_alias_real_records(setup, invalid_id):
    repo, owner, _, student, _, _, _, _ = setup

    with pytest.raises(LookupError, match="User not found"):
        repo.list_courses(invalid_id)
    with pytest.raises(LookupError, match="Course not found"):
        repo.create_assessment(owner.id, invalid_id, "Bad ID", Decimal("100"))
    with pytest.raises(LookupError, match="Assessment not found"):
        repo.set_grade(owner.id, invalid_id, student.id, Decimal("5"))


def test_repository_instances_are_isolated_and_read_lists_cannot_change_storage(setup):
    repo, owner, _, _, _, _, _, _ = setup
    other = InMemoryGradebookRepository()

    with pytest.raises(LookupError, match="User not found"):
        other.list_courses(owner.id)
    courses = repo.list_courses(owner.id)
    courses.clear()
    assert len(repo.list_courses(owner.id)) == 1
    assert repo.healthy() is True
