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


def test_enrollment_makes_course_visible_to_student(setup):
    app, _, owner, student, visible, hidden = setup
    student_client = signed_in_client(app, student)
    assert [course["id"] for course in student_client.get(COURSES).get_json()] == [visible.id]

    url = f"{COURSES}/{hidden.id}/enrollments/{student.id}"
    owner_client = signed_in_client(app, owner)
    for _ in range(2):
        response = owner_client.put(url, headers=CSRF_HEADER)
        assert response.status_code == 200
        assert response.get_json() == {"course_id": hidden.id, "student_id": student.id}
    assert {course["id"] for course in student_client.get(COURSES).get_json()} == {
        visible.id,
        hidden.id,
    }


def test_enrollment_requires_course_owner_and_csrf(setup):
    app, owner, other, student, visible, _ = setup
    url = f"{COURSES}/{visible.id}/enrollments/{student.id}"

    for user in (other, student):
        response = signed_in_client(app, user).put(url, headers=CSRF_HEADER)
        assert response.status_code == 403
    assert signed_in_client(app, owner).put(url).status_code == 400


def test_enrollment_rejects_missing_accounts_and_lecturers(setup):
    app, owner, other, _, visible, _ = setup
    client = signed_in_client(app, owner)
    url = f"{COURSES}/{visible.id}/enrollments"

    assert client.put(f"{url}/999", headers=CSRF_HEADER).status_code == 404
    assert client.put(f"{url}/{other.id}", headers=CSRF_HEADER).status_code == 400


def test_owner_creates_assessment_and_enrolled_student_can_read_it(setup):
    app, owner, other, student, visible, hidden = setup
    url = f"{COURSES}/{visible.id}/assessments"
    client = signed_in_client(app, owner)

    response = client.post(url, json={"name": " Project ", "weight": "40.50"}, headers=CSRF_HEADER)
    assert response.status_code == 201
    assessment = response.get_json()
    assert assessment == {
        "id": assessment["id"],
        "course_id": visible.id,
        "name": "Project",
        "weight": "40.50",
    }
    assert client.get(url).get_json() == [assessment]
    student_client = signed_in_client(app, student)
    assert student_client.get(url).get_json() == [assessment]
    assert student_client.get(f"{COURSES}/{hidden.id}/assessments").status_code == 403
    assert signed_in_client(app, other).get(url).status_code == 403


def test_assessment_creation_checks_permissions_and_course(setup):
    app, owner, other, student, visible, _ = setup
    url = f"{COURSES}/{visible.id}/assessments"
    payload = {"name": "Project", "weight": "40"}
    for user in (other, student):
        response = signed_in_client(app, user).post(url, json=payload, headers=CSRF_HEADER)
        assert response.status_code == 403

    client = signed_in_client(app, owner)
    assert client.post(url, json=payload).status_code == 400
    assert client.get(f"{COURSES}/999/assessments").status_code == 404
    assert (
        client.post(f"{COURSES}/999/assessments", json=payload, headers=CSRF_HEADER).status_code
        == 404
    )
    assert client.get(url).get_json() == []


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"weight": "40"},
        {"name": " ", "weight": "40"},
        {"name": "Project", "weight": 40.5},
        {"name": "Project", "weight": "0"},
        {"name": "Project", "weight": "NaN"},
        {"name": "Project", "weight": "1e-99999999"},
        {"name": "Project", "weight": "1" * 33},
    ],
)
def test_invalid_assessment_input_is_rejected(setup, payload):
    app, owner, _, _, visible, _ = setup
    client = signed_in_client(app, owner)
    url = f"{COURSES}/{visible.id}/assessments"

    assert client.post(url, json=payload, headers=CSRF_HEADER).status_code == 400
    assert client.get(url).get_json() == []
