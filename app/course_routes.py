"""Course API backed by the signed-in user's repository permissions."""

import re
from decimal import Decimal

from flask import Blueprint, current_app, g, jsonify, request

from app.auth import login_required

bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def course_json(course):
    return {"id": course.id, "name": course.name, "lecturer_id": course.lecturer_id}


def assessment_json(assessment):
    return {
        "id": assessment.id,
        "course_id": assessment.course_id,
        "name": assessment.name,
        "weight": str(assessment.weight),
    }


@bp.get("")
@login_required
def list_courses():
    repository = current_app.extensions["repository"]
    return jsonify([course_json(course) for course in repository.list_courses(g.user.id)])


@bp.post("")
@login_required
def create_course():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
        return jsonify(error="Provide a course name"), 400

    repository = current_app.extensions["repository"]
    try:
        course = repository.create_course(g.user.id, payload["name"].strip())
    except PermissionError:
        return jsonify(error="Only lecturers can create courses"), 403
    except ValueError:
        return jsonify(error="Provide a course name"), 400
    return jsonify(course_json(course)), 201


@bp.put("/<int:course_id>/enrollments/<int:student_id>")
@login_required
def enroll_student(course_id, student_id):
    repository = current_app.extensions["repository"]
    try:
        enrollment = repository.enroll_student(g.user.id, course_id, student_id)
    except PermissionError:
        return jsonify(error="Only the course owner can enroll students"), 403
    except LookupError:
        return jsonify(error="Course or student account not found"), 404
    except ValueError:
        return jsonify(error="Only student accounts can be enrolled"), 400
    return jsonify(course_id=enrollment.course_id, student_id=enrollment.student_id)


@bp.get("/<int:course_id>/assessments")
@login_required
def list_assessments(course_id):
    repository = current_app.extensions["repository"]
    try:
        assessments = repository.list_assessments(g.user.id, course_id)
    except PermissionError:
        return jsonify(error="You do not have access to this course"), 403
    except LookupError:
        return jsonify(error="Course not found"), 404
    return jsonify([assessment_json(assessment) for assessment in assessments])


@bp.post("/<int:course_id>/assessments")
@login_required
def create_assessment(course_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
        return jsonify(error="Provide an assessment name"), 400

    weight = payload.get("weight")
    if (
        not isinstance(weight, str)
        or len(weight) > 32
        or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", weight)
    ):
        return jsonify(error="Provide a decimal weight as text, such as '40.5'"), 400

    repository = current_app.extensions["repository"]
    try:
        assessment = repository.create_assessment(
            g.user.id, course_id, payload["name"].strip(), Decimal(weight)
        )
    except PermissionError:
        return jsonify(error="Only the course owner can add assessments"), 403
    except LookupError:
        return jsonify(error="Course not found"), 404
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(assessment_json(assessment)), 201
