"""Course API backed by the signed-in user's repository permissions."""

from flask import Blueprint, current_app, g, jsonify, request

from app.auth import login_required

bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def course_json(course):
    return {"id": course.id, "name": course.name, "lecturer_id": course.lecturer_id}


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
