"""Exercise course permissions through Flask's HTTP interface."""

import pytest

from app import create_app
from app.models import Role
from app.repository import InMemoryGradebookRepository

COURSES = "/api/courses"
CSRF_HEADER = {"X-CSRF-Token": "test-token"}


@pytest.fixture
def setup():
    repo = InMemoryGradebookRepository()
    lecturer = repo.create_user("lecturer", Role.LECTURER, "unused-test-hash")
    other = repo.create_user("other", Role.LECTURER, "unused-test-hash")
    student = repo.create_user("student", Role.STUDENT, "unused-test-hash")
    visible = repo.create_course(lecturer.id, "DevOps")
    hidden = repo.create_course(other.id, "Statistics")
    repo.enroll_student(lecturer.id, visible.id, student.id)
    app = create_app(repository=repo, config={"TESTING": True, "SECRET_KEY": "test-only"})
    return app, lecturer, other, student, visible, hidden


def signed_in_client(app, user):
    client = app.test_client()
    with client.session_transaction() as browser_session:
        browser_session["user_id"] = user.id
        browser_session["csrf_token"] = CSRF_HEADER["X-CSRF-Token"]
    return client


def test_anonymous_user_cannot_list_courses(setup):
    app, *_ = setup
    assert app.test_client().get(COURSES).status_code == 401


def test_each_role_only_sees_its_courses(setup):
    app, lecturer, other, student, visible, hidden = setup
    for user, expected in ((lecturer, visible), (student, visible), (other, hidden)):
        response = signed_in_client(app, user).get(COURSES)
        assert response.status_code == 200
        assert response.get_json() == [
            {"id": expected.id, "name": expected.name, "lecturer_id": expected.lecturer_id}
        ]


def test_course_owner_comes_from_session(setup):
    app, lecturer, other, *_ = setup
    client = signed_in_client(app, lecturer)
    response = client.post(
        COURSES, json={"name": " Databases ", "lecturer_id": other.id}, headers=CSRF_HEADER
    )
    assert response.status_code == 201
    course = response.get_json()
    assert course["lecturer_id"] == lecturer.id
    assert course["name"] == "Databases"
    assert course in client.get(COURSES).get_json()


def test_student_cannot_create_courses(setup):
    app, lecturer, _, student, *_ = setup
    response = signed_in_client(app, student).post(
        COURSES, json={"name": "Databases", "actor_id": lecturer.id}, headers=CSRF_HEADER
    )
    assert response.status_code == 403


@pytest.mark.parametrize("payload", [[], {}, {"name": 12}, {"name": "  "}])
def test_invalid_course_name_is_rejected(setup, payload):
    app, lecturer, *_ = setup
    response = signed_in_client(app, lecturer).post(COURSES, json=payload, headers=CSRF_HEADER)
    assert response.status_code == 400


def test_course_creation_requires_csrf_token(setup):
    app, lecturer, *_ = setup
    response = signed_in_client(app, lecturer).post(COURSES, json={"name": "Databases"})
    assert response.status_code == 400
